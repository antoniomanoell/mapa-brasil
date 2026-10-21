"""`gini` — Índice de Gini da renda domiciliar per capita (ver DECISIONS.md).

Dois segmentos, nunca emendados: PNAD anual 2001–2015 (microdados, mesmo conceito da renda_pc)
e PNAD Contínua 2012+ (SIDRA 7435).
"""

from datetime import date

from ..escala import escala_quantil
from ..raw_manual import carregar_manifest
from ..schema import Flag, Indicador, Ponto, Quebra, Segmento, Subindicador
from ..sources import ibge_pnad_microdados as pnad
from ..sources import ibge_sidra
from ..validate import LIMIAR_CV_PADRAO, Auxiliares, Regras, ultimo_ano_transcorrido
from .renda_pc import FIM_COBERTURA_URBANA, UFS_COBERTURA_URBANA

TABELA = 7435
VAR_VALOR = 10681
VAR_CV = 10682
CASAS = 3
# Conferência indireta do segmento PNAD: SIS 2016, Tabela 6.3 (Gini do rendimento de todas as
# fontes das pessoas de 15 anos ou mais com rendimento), calculado com o mesmo código.
AUX_SIS = "sis2016_tab6_3"


class Gini:
    id = "gini"
    regras = Regras(
        faixa=(0, 1),
        limiar_variacao=0.08,
        metodologias={"pnad": (2001, 2015), "pnadc": (2012, None)},
    )

    def __init__(self) -> None:
        self.auxiliares: Auxiliares = {}

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        segmentos = [self._segmento_pnad(), self._segmento_pnadc(hoje)]
        return Indicador(
            id=self.id,
            nome="Índice de Gini da renda domiciliar per capita",
            tema="Renda",
            unidade="índice",
            unidade_detalhe="índice de 0 (igualdade) a 1 (desigualdade máxima)",
            direcao="menor_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[Subindicador(id="principal", nome="Índice de Gini")],
            segmentos=segmentos,
            quebras=[
                Quebra(
                    ano=2012,
                    texto=(
                        "Mudança de pesquisa: PNAD → PNAD Contínua. A amostra, o questionário e a "
                        "captação dos rendimentos mudaram; as séries não são diretamente "
                        "comparáveis. De 2012 a 2015 os dois valores são mostrados."
                    ),
                )
            ],
            escalas={"principal": escala_quantil(segmentos, CASAS)},
            versao_pipeline=versao_pipeline,
        )

    def _segmento_pnadc(self, hoje: date) -> Segmento:
        inicio, fim_tabela = ibge_sidra.periodo(TABELA)
        fim = min(fim_tabela, ultimo_ano_transcorrido(hoje))
        dados, obtido_em = ibge_sidra.consultar(TABELA, [VAR_VALOR, VAR_CV], (inicio, fim))
        anos = list(range(inicio, fim + 1))
        valores: dict[str, dict[str, Ponto]] = {}
        for geo, serie in sorted(dados[VAR_VALOR].items()):
            for ano in anos:
                v = serie.get(ano)
                cv = dados[VAR_CV].get(geo, {}).get(ano)
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
            fonte="IBGE – PNAD Contínua anual (rendimento de todas as fontes)",
            fonte_url=ibge_sidra.url_tabela(TABELA),
            tabela=f"SIDRA {TABELA}, variáveis {VAR_VALOR} (índice) e {VAR_CV} (CV)",
            extraido_em=obtido_em,
            notas=(
                "Segundo o IBGE, de 2020 a 2022 os dados vêm da 5ª visita da PNAD Contínua; nos "
                "demais anos, da 1ª."
            ),
            anos=anos,
            valores=valores,
        )

    def _segmento_pnad(self) -> Segmento:
        anos = pnad.ANOS
        valores: dict[str, dict[str, Ponto]] = {}
        for ano in anos:
            renda = pnad.renda_ano(ano)
            for geo, g in renda.gini.items():
                flags = []
                if geo in UFS_COBERTURA_URBANA and ano <= FIM_COBERTURA_URBANA:
                    flags.append(Flag.COBERTURA_URBANA)
                valores.setdefault(geo, {})[str(ano)] = Ponto(v=round(g, 3), flags=flags)
            for geo, g in renda.gini_individual_sis.items():
                self.auxiliares[(AUX_SIS, "principal", "pnad", geo, ano)] = round(g, 3)

        manifest = carregar_manifest()
        baixado_em = max(manifest[a].baixado_em for ano in anos for a in pnad.ARQUIVOS[ano] if a)
        return Segmento(
            id="pnad",
            subindicador="principal",
            rotulo=f"PNAD ({anos[0]}–{anos[-1]})",
            fonte="IBGE – PNAD anual, microdados (cálculo do projeto)",
            fonte_url=pnad.URL_MICRODADOS,
            tabela=(
                "Microdados da PNAD; 2001–2012 com os pesos reponderados pela Projeção da "
                "População de 2013."
            ),
            extraido_em=baixado_em,
            notas=(
                "Calculado pelo projeto a partir dos microdados da PNAD, com a mesma renda per "
                "capita do indicador de renda (por pessoa, incluindo quem mora em domicílio sem "
                "rendimento). Sem dados em 2010: ano de Censo, a PNAD não foi a campo. "
                f"Até {FIM_COBERTURA_URBANA} a PNAD não cobria a área rural de RO, AC, AM, RR, "
                "PA e AP (marcados como cobertura apenas urbana). O mesmo cálculo reproduz o Gini "
                "publicado na Síntese de Indicadores Sociais 2016 (Tabela 6.3) quando feito no "
                "conceito dela. Não há CV publicado nem calculado para este segmento."
            ),
            anos=anos,
            valores=valores,
        )
