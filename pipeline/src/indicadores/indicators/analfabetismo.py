"""`analfabetismo` — taxa de analfabetismo das pessoas de 15 anos ou mais.

Dois segmentos, nunca emendados: PNAD anual 2001–2015 (SIDRA 271, contagens por idade e
alfabetização) e PNAD Contínua 2016+ (SIDRA 7113, taxa publicada com CV).
"""

from datetime import date

from ..escala import escala_quantil
from ..schema import Flag, Indicador, Ponto, Quebra, Segmento, Subindicador
from ..sources import ibge_sidra
from ..validate import LIMIAR_CV_PADRAO, Regras, ultimo_ano_transcorrido
from .renda_pc import FIM_COBERTURA_URBANA, UFS_COBERTURA_URBANA

CASAS = 1

# PNADC: tabela 7113, sexo Total (6794), grupo de idade "15 anos ou mais" (2795).
PNADC_TABELA = 7113
PNADC_VAR = 10267
PNADC_CV = 10268
PNADC_CLASSES = "2[6794]|58[2795]"

# PNAD: tabela 271 (pessoas de 5 anos ou mais), situação Total, sexo Total.
PNAD_TABELA = 271
PNAD_VAR = 121
ALFABETIZADAS = "1023"
NAO_ALFABETIZADAS = "1024"
# Grupos de idade que somam exatamente "15 anos ou mais" (sem sobreposição e sem idade ignorada).
GRUPOS_15_OU_MAIS = ["1143", "1144", "1145", "3299", "3300", "3301", "3302"]
PNAD_CLASSES = (
    f"1[0]|2[0]|59[{ALFABETIZADAS},{NAO_ALFABETIZADAS}]|58[{','.join(GRUPOS_15_OU_MAIS)}]"
)


class Analfabetismo:
    id = "analfabetismo"
    regras = Regras(
        faixa=(0, 100),
        limiar_variacao=0.2,
        metodologias={"pnad": (2001, 2015), "pnadc": (2016, None)},
    )

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        segmentos = [self._segmento_pnad(), self._segmento_pnadc(hoje)]
        return Indicador(
            id=self.id,
            nome="Taxa de analfabetismo (15 anos ou mais)",
            tema="Educação",
            unidade="%",
            unidade_detalhe="% das pessoas de 15 anos ou mais que não sabem ler e escrever",
            direcao="menor_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[Subindicador(id="principal", nome="Taxa de analfabetismo")],
            segmentos=segmentos,
            quebras=[
                Quebra(
                    ano=2016,
                    texto=(
                        "Mudança de pesquisa: PNAD → PNAD Contínua. A taxa da PNAD Contínua começa "
                        "em 2016; as séries não são diretamente comparáveis."
                    ),
                )
            ],
            escalas={"principal": escala_quantil(segmentos, CASAS)},
            versao_pipeline=versao_pipeline,
        )

    def _segmento_pnadc(self, hoje: date) -> Segmento:
        inicio, fim_tabela = ibge_sidra.periodo(PNADC_TABELA)
        fim = min(fim_tabela, ultimo_ano_transcorrido(hoje))
        dados, obtido_em = ibge_sidra.consultar(
            PNADC_TABELA, [PNADC_VAR, PNADC_CV], (inicio, fim), PNADC_CLASSES
        )
        anos = list(range(inicio, fim + 1))
        valores: dict[str, dict[str, Ponto]] = {}
        for geo, serie in sorted(dados[PNADC_VAR].items()):
            for ano in anos:
                v = serie.get(ano)
                cv = dados[PNADC_CV].get(geo, {}).get(ano)
                if v is None:
                    ponto = Ponto(v=None, lacuna="valor não publicado pelo IBGE")
                else:
                    alto = cv is not None and cv > LIMIAR_CV_PADRAO
                    ponto = Ponto(v=v, cv=cv, flags=[Flag.BAIXA_PRECISAO] if alto else [])
                valores.setdefault(geo, {})[str(ano)] = ponto
        return Segmento(
            id="pnadc",
            subindicador="principal",
            rotulo=f"PNAD Contínua ({inicio}–)",
            fonte="IBGE – PNAD Contínua anual (educação)",
            fonte_url=ibge_sidra.url_tabela(PNADC_TABELA),
            tabela=(
                f"SIDRA {PNADC_TABELA}, variáveis {PNADC_VAR} (taxa) e {PNADC_CV} (CV), "
                f"classificações {PNADC_CLASSES}"
            ),
            extraido_em=obtido_em,
            notas="Taxa publicada pelo IBGE.",
            anos=anos,
            valores=valores,
        )

    def _segmento_pnad(self) -> Segmento:
        inicio, fim = ibge_sidra.periodo(PNAD_TABELA)
        dados, obtido_em = ibge_sidra.consultar_categorias(
            PNAD_TABELA, [PNAD_VAR], (inicio, fim), PNAD_CLASSES
        )
        # Soma os grupos de idade, separando alfabetizadas e não alfabetizadas.
        soma: dict[str, dict[str, dict[int, float]]] = {ALFABETIZADAS: {}, NAO_ALFABETIZADAS: {}}
        for cats, por_geo in dados[PNAD_VAR].items():
            alfab = next(c for c in cats if c in soma)
            for geo, serie in por_geo.items():
                for ano, v in serie.items():
                    if v is not None:
                        alvo = soma[alfab].setdefault(geo, {})
                        alvo[ano] = alvo.get(ano, 0.0) + v
        anos = sorted({a for serie in soma[NAO_ALFABETIZADAS].values() for a in serie})
        valores: dict[str, dict[str, Ponto]] = {}
        for geo in sorted(soma[NAO_ALFABETIZADAS]):
            for ano in anos:
                nao = soma[NAO_ALFABETIZADAS][geo][ano]
                total = nao + soma[ALFABETIZADAS][geo][ano]
                flags = []
                if geo in UFS_COBERTURA_URBANA and ano <= FIM_COBERTURA_URBANA:
                    flags.append(Flag.COBERTURA_URBANA)
                valores.setdefault(geo, {})[str(ano)] = Ponto(
                    v=round(nao / total * 100, 2), flags=flags
                )
        return Segmento(
            id="pnad",
            subindicador="principal",
            rotulo=f"PNAD ({anos[0]}–{anos[-1]})",
            fonte="IBGE – PNAD anual",
            fonte_url=ibge_sidra.url_tabela(PNAD_TABELA),
            tabela=(
                f"SIDRA {PNAD_TABELA}, variável {PNAD_VAR}: não alfabetizadas ÷ (alfabetizadas + "
                "não alfabetizadas), somando os grupos de idade de 15 anos ou mais"
            ),
            extraido_em=obtido_em,
            notas=(
                "Taxa calculada pelo projeto a partir das contagens publicadas pelo IBGE (pessoas "
                "por alfabetização e grupo de idade); a idade ignorada fica de fora. Sem dados em "
                f"2010: ano de Censo, a PNAD não foi a campo. Até {FIM_COBERTURA_URBANA} a PNAD "
                "não cobria a área rural de RO, AC, AM, RR, PA e AP (marcados como cobertura "
                "apenas urbana). Não há CV publicado para este segmento."
            ),
            anos=anos,
            valores=valores,
        )
