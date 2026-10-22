"""`analfabetismo` — taxa de analfabetismo das pessoas de 15 anos ou mais.

Dois segmentos, nunca emendados: PNAD anual 2001–2015 (microdados, cálculo do projeto com CV; ver
DECISIONS.md) e PNAD Contínua 2016+ (SIDRA 7113, taxa publicada com CV).
"""

from datetime import date

from ..escala import escala_quantil
from ..raw_manual import carregar_manifest
from ..schema import Flag, Indicador, Ponto, Quebra, Segmento, Subindicador
from ..sources import ibge_pnad_microdados as pnad
from ..sources import ibge_sidra
from ..validate import LIMIAR_CV_PADRAO, Regras, ultimo_ano_transcorrido
from .renda_pc import FIM_COBERTURA_URBANA, UFS_COBERTURA_URBANA

CASAS = 1

# PNADC: tabela 7113, sexo Total (6794), grupo de idade "15 anos ou mais" (2795).
PNADC_TABELA = 7113
PNADC_VAR = 10267
PNADC_CV = 10268
PNADC_CLASSES = "2[6794]|58[2795]"


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
        anos = pnad.ANOS
        valores: dict[str, dict[str, Ponto]] = {}
        for ano in anos:
            for geo, est in pnad.renda_ano(ano).analfabetismo.items():
                cv = round(est.cv, 1) if est.cv is not None else None
                flags = [Flag.BAIXA_PRECISAO] if cv is not None and cv > LIMIAR_CV_PADRAO else []
                if geo in UFS_COBERTURA_URBANA and ano <= FIM_COBERTURA_URBANA:
                    flags.append(Flag.COBERTURA_URBANA)
                valores.setdefault(geo, {})[str(ano)] = Ponto(
                    v=round(est.media, 2), cv=cv, flags=flags
                )
        manifest = carregar_manifest()
        baixado_em = max(manifest[a].baixado_em for ano in anos for a in pnad.ARQUIVOS[ano] if a)
        return Segmento(
            id="pnad",
            subindicador="principal",
            rotulo=f"PNAD ({anos[0]}–{anos[-1]})",
            fonte="IBGE – PNAD anual, microdados (cálculo do projeto)",
            fonte_url=pnad.URL_MICRODADOS,
            tabela=(
                "Microdados da PNAD (V0601 e V8005, peso V4729); 2001–2012 com os pesos "
                "reponderados pela Projeção da População de 2013."
            ),
            extraido_em=baixado_em,
            notas=(
                "Calculado pelo projeto a partir dos microdados da PNAD: pessoas de 15 anos ou "
                "mais que não sabem ler e escrever. O mesmo cálculo reproduz a taxa do Brasil "
                "publicada na Síntese de Indicadores Sociais 2016 (Tabela 4.15). Sem dados em "
                f"2010: ano de Censo, a PNAD não foi a campo. Até {FIM_COBERTURA_URBANA} a PNAD "
                "não cobria a área rural de RO, AC, AM, RR, PA e AP (marcados como cobertura "
                "apenas urbana)."
            ),
            anos=anos,
            valores=valores,
        )
