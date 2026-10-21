"""`pobreza` e `extrema_pobreza` — proporção abaixo das linhas do Banco Mundial (SIS do IBGE).

Exatamente a série publicada na Síntese de Indicadores Sociais (PROJECT.md, 4.1). Todos os anos vêm
da mesma edição (2025), que recalcula a série inteira com o mesmo método.
"""

from datetime import date

from ..escala import escala_quantil
from ..raw_manual import carregar_manifest
from ..schema import Flag, Indicador, Ponto, Segmento, Subindicador
from ..sources import ibge_sis
from ..validate import LIMIAR_CV_PADRAO, Regras, ultimo_ano_transcorrido

CASAS = 1


class PobrezaSis:
    def __init__(self, id_: str, linha: str, nome: str, linha_texto: str, regras: Regras) -> None:
        self.id = id_
        self.linha = linha
        self.nome = nome
        self.linha_texto = linha_texto
        self.regras = regras

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        tab = ibge_sis.tabela_2_23()
        serie = tab.valores[self.linha]
        anos = sorted(a for a in tab.fontes if a <= ultimo_ano_transcorrido(hoje))
        valores: dict[str, dict[str, Ponto]] = {}
        for geo, por_ano in sorted(serie.items()):
            for ano in anos:
                p = por_ano[ano]
                cv = round(p.cv, 1) if p.cv is not None else None
                alto = cv is not None and cv > LIMIAR_CV_PADRAO
                valores.setdefault(geo, {})[str(ano)] = Ponto(
                    v=round(p.v, 2), cv=cv, flags=[Flag.BAIXA_PRECISAO] if alto else []
                )
        quintas = [a for a in anos if "quintas" in tab.fontes[a]]
        seg = Segmento(
            id="sis_pnadc",
            subindicador="principal",
            rotulo=f"SIS 2025 – PNAD Contínua ({anos[0]}–{anos[-1]})",
            fonte="IBGE – Síntese de Indicadores Sociais 2025 (PNAD Contínua)",
            fonte_url=ibge_sis.URL,
            tabela=f"{ibge_sis.TABELA} (2_Distribuicao_Renda_xls.zip), coluna {self.linha}",
            extraido_em=carregar_manifest()[ibge_sis.ARQUIVO].baixado_em,
            notas=(
                f"Pessoas com rendimento domiciliar per capita abaixo de {self.linha_texto}, "
                "linha do Banco Mundial convertida pelo IBGE em reais de cada ano. Série publicada "
                "pelo IBGE na SIS 2025, que recalcula todos os anos com o mesmo método. "
                f"Em {', '.join(map(str, quintas))} os dados vêm da 5ª visita da PNAD Contínua; "
                "nos demais anos, da 1ª. O Banco Mundial atualizou suas linhas em 2025; segundo o "
                "IBGE, a mudança entra na próxima edição da SIS, e a série será revista."
            ),
            anos=anos,
            valores=valores,
        )
        return Indicador(
            id=self.id,
            nome=self.nome,
            tema="Pobreza",
            unidade="%",
            unidade_detalhe=f"% da população abaixo de {self.linha_texto}",
            direcao="menor_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[Subindicador(id="principal", nome=self.nome)],
            segmentos=[seg],
            escalas={"principal": escala_quantil([seg], CASAS)},
            versao_pipeline=versao_pipeline,
        )


def pobreza() -> PobrezaSis:
    return PobrezaSis(
        "pobreza",
        "US$ 6,85 PPC 2017",
        "Pobreza",
        "US$ 6,85 por dia (PPC 2017)",
        Regras(faixa=(0, 100), limiar_variacao=0.25, metodologias={"sis_pnadc": (2012, None)}),
    )


def extrema_pobreza() -> PobrezaSis:
    return PobrezaSis(
        "extrema_pobreza",
        "US$ 2,15 PPC 2017",
        "Extrema pobreza",
        "US$ 2,15 por dia (PPC 2017)",
        Regras(faixa=(0, 100), limiar_variacao=0.35, metodologias={"sis_pnadc": (2012, None)}),
    )
