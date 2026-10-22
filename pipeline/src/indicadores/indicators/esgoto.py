"""`esgoto` — % de domicílios com esgotamento sanitário adequado (ver DECISIONS.md).

"Adequado" = rede geral ou pluvial, ou fossa (séptica) ligada à rede. Denominador do IBGE:
domicílios com banheiro, sanitário ou buraco para dejeções. Três segmentos, nunca emendados:
PNAD anual 2001–2015 (microdados), PNAD Contínua 2016–2018 (SIDRA 6735) e 2019+ (SIDRA 7192),
porque o IBGE mudou as categorias em 2019.
"""

from datetime import date

from ..escala import escala_quantil
from ..raw_manual import carregar_manifest
from ..schema import Flag, Indicador, Ponto, Quebra, Segmento, Subindicador
from ..sources import ibge_pnad_microdados as pnad
from ..sources import ibge_sidra
from ..validate import LIMIAR_CV_PADRAO, Auxiliares, Regras, ultimo_ano_transcorrido
from .renda_pc import FIM_COBERTURA_URBANA, UFS_COBERTURA_URBANA

CASAS = 1

# PNADC: % dos domicílios com banheiro/sanitário (var. 9988) e CV (9989), situação Total.
VAR_PCT = 9988
VAR_PCT_CV = 9989
PNADC_2016 = 6735  # 2016–2018: "Rede geral, rede pluvial ou fossa ligada à rede" = 46290
PNADC_2016_ADEQUADO = ["46290"]
PNADC_2019 = (
    7192  # 2019+: "Rede geral ou rede pluvial" = 47930; "Fossa séptica ligada à rede" = 47931
)
PNADC_2019_ADEQUADO = ["47930", "47931"]

# Conferência do segmento PNAD: domicílios (mil) ligados à rede, contra a SIDRA 1956 (2009+), que
# publica "rede coletora" e "fossa séptica ligada à rede coletora" em milhares.
AUX_SIDRA = "sidra1956_rede_mil"

NOTA_DENOMINADOR = (
    "Percentual sobre os domicílios que têm banheiro, sanitário ou buraco para dejeções, como o "
    "IBGE publica: domicílios sem nenhum deles ficam fora da conta."
)


class Esgoto:
    id = "esgoto"
    regras = Regras(
        faixa=(0, 100),
        limiar_variacao=0.2,
        metodologias={"pnad": (2001, 2015), "pnadc2016": (2016, 2018), "pnadc2019": (2019, None)},
    )

    def __init__(self) -> None:
        self.auxiliares: Auxiliares = {}

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        segmentos = [
            self._segmento_pnad(),
            self._segmento_pnadc(
                hoje,
                "pnadc2016",
                PNADC_2016,
                PNADC_2016_ADEQUADO,
                "PNAD Contínua (2016–2018)",
                "Categoria do IBGE: rede geral, rede pluvial ou fossa ligada à rede.",
            ),
            self._segmento_pnadc(
                hoje,
                "pnadc2019",
                PNADC_2019,
                PNADC_2019_ADEQUADO,
                "PNAD Contínua (2019–)",
                "Soma das categorias do IBGE: rede geral ou rede pluvial; fossa séptica ligada à "
                "rede. Sem CV: o IBGE publica o CV de cada categoria, não o da soma.",
            ),
        ]
        return Indicador(
            id=self.id,
            nome="Domicílios com esgotamento sanitário adequado",
            tema="Saneamento",
            unidade="%",
            unidade_detalhe=(
                "% dos domicílios com banheiro ou sanitário ligados à rede geral ou pluvial, "
                "direto ou por fossa"
            ),
            direcao="maior_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[Subindicador(id="principal", nome="Esgotamento adequado")],
            segmentos=segmentos,
            quebras=[
                Quebra(
                    ano=2016,
                    texto=(
                        "Mudança de pesquisa: PNAD → PNAD Contínua. As séries não são "
                        "diretamente comparáveis."
                    ),
                ),
                Quebra(
                    ano=2019,
                    texto=(
                        "O IBGE mudou as categorias de esgotamento sanitário da PNAD Contínua: "
                        "a partir de 2019 a fossa séptica ligada à rede é investigada à parte."
                    ),
                ),
            ],
            escalas={"principal": escala_quantil(segmentos, CASAS)},
            versao_pipeline=versao_pipeline,
        )

    def _segmento_pnadc(
        self,
        hoje: date,
        id_: str,
        tabela: int,
        adequado: list[str],
        rotulo: str,
        nota: str,
    ) -> Segmento:
        inicio, fim_tabela = ibge_sidra.periodo(tabela)
        fim = min(fim_tabela, ultimo_ano_transcorrido(hoje))
        classes = f"1[6795]|11558[{','.join(adequado)}]"
        dados, obtido_em = ibge_sidra.consultar_categorias(
            tabela, [VAR_PCT, VAR_PCT_CV], (inicio, fim), classes
        )
        anos = list(range(inicio, fim + 1))
        partes = list(dados[VAR_PCT].values())
        valores: dict[str, dict[str, Ponto]] = {}
        for geo in sorted(partes[0]):
            for ano in anos:
                vs = [p[geo].get(ano) for p in partes]
                if any(v is None for v in vs):
                    ponto = Ponto(v=None, lacuna="valor não publicado pelo IBGE")
                elif len(partes) == 1:
                    cv = next(iter(dados[VAR_PCT_CV].values()))[geo].get(ano)
                    alto = cv is not None and cv > LIMIAR_CV_PADRAO
                    ponto = Ponto(v=vs[0], cv=cv, flags=[Flag.BAIXA_PRECISAO] if alto else [])
                else:
                    ponto = Ponto(v=round(sum(vs), 1))  # type: ignore[arg-type]
                valores.setdefault(geo, {})[str(ano)] = ponto
        return Segmento(
            id=id_,
            subindicador="principal",
            rotulo=rotulo,
            fonte="IBGE – PNAD Contínua anual (características dos domicílios)",
            fonte_url=ibge_sidra.url_tabela(tabela),
            tabela=f"SIDRA {tabela}, variável {VAR_PCT} (%), classificações {classes}",
            extraido_em=obtido_em,
            notas=f"{nota} {NOTA_DENOMINADOR}",
            anos=anos,
            valores=valores,
        )

    def _segmento_pnad(self) -> Segmento:
        anos = pnad.ANOS
        valores: dict[str, dict[str, Ponto]] = {}
        for ano in anos:
            resultado = pnad.renda_ano(ano)
            for geo, est in resultado.esgoto.items():
                cv = round(est.cv, 1) if est.cv is not None else None
                flags = [Flag.BAIXA_PRECISAO] if cv is not None and cv > LIMIAR_CV_PADRAO else []
                if geo in UFS_COBERTURA_URBANA and ano <= FIM_COBERTURA_URBANA:
                    flags.append(Flag.COBERTURA_URBANA)
                valores.setdefault(geo, {})[str(ano)] = Ponto(
                    v=round(est.media, 2), cv=cv, flags=flags
                )
            for geo, c in resultado.esgoto_contagens.items():
                self.auxiliares[(AUX_SIDRA, "principal", "pnad", geo, ano)] = round(c["rede"], 2)
        manifest = carregar_manifest()
        baixado_em = max(manifest[a].baixado_em for ano in anos for a in pnad.ARQUIVOS[ano] if a)
        return Segmento(
            id="pnad",
            subindicador="principal",
            rotulo=f"PNAD ({anos[0]}–{anos[-1]})",
            fonte="IBGE – PNAD anual, microdados (cálculo do projeto)",
            fonte_url=pnad.URL_MICRODADOS,
            tabela=(
                "Microdados da PNAD (V0217, domicílios particulares permanentes, peso V4611): "
                "(rede coletora + fossa séptica ligada à rede) ÷ domicílios com banheiro ou "
                "sanitário; 2001–2012 com os pesos reponderados pela Projeção da População de 2013."
            ),
            extraido_em=baixado_em,
            notas=(
                "Calculado pelo projeto a partir dos microdados da PNAD, com a mesma definição em "
                "todos os anos (a tabela SIDRA 1956 só separa a fossa ligada à rede a partir de "
                "2009). Sem dados em 2010: ano de Censo, a PNAD não foi a campo. "
                f"Até {FIM_COBERTURA_URBANA} a PNAD não cobria a área rural de RO, AC, AM, RR, PA "
                f"e AP (marcados como cobertura apenas urbana). {NOTA_DENOMINADOR}"
            ),
            anos=anos,
            valores=valores,
        )
