"""`esperanca_vida` e `mort_infantil` — estimativas do IBGE nas Projeções da População (rev. 2024).

Ver DECISIONS.md: as séries vão só até o último ano com Tábua Completa de Mortalidade publicada.
"""

from datetime import date

from ..escala import escala_quantil
from ..raw_manual import carregar_manifest
from ..schema import Flag, Indicador, Ponto, Segmento, Subindicador
from ..sources import ibge_projecoes
from ..sources.datasus_tabnet import SIM, SIM_FAIXA_MENOR_1_ANO, SINASC
from ..validate import Regras, ultimo_ano_transcorrido

# Último ano com Tábua Completa de Mortalidade publicada pelo IBGE (a de 2024 saiu em 28/11/2025).
# Atualizar quando sair a próxima Tábua, conferindo o valor nela.
ULTIMO_ANO_TABUA = 2024
ANO_INICIAL = 2000


class IndicadorProjecao:
    def __init__(
        self,
        id_: str,
        coluna: str,
        nome: str,
        tema: str,
        unidade: str,
        unidade_detalhe: str,
        direcao: str,
        casas: int,
        regras: Regras,
    ) -> None:
        self.id = id_
        self.coluna = coluna
        self.nome = nome
        self.tema = tema
        self.unidade = unidade
        self.unidade_detalhe = unidade_detalhe
        self.direcao = direcao
        self.casas = casas
        self.regras = regras

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        fim = min(ultimo_ano_transcorrido(hoje), ULTIMO_ANO_TABUA)
        serie = ibge_projecoes.serie(self.coluna, fim)
        anos = list(range(ANO_INICIAL, fim + 1))
        valores = {
            geo: {str(a): Ponto(v=round(por_ano[a], 2), flags=[Flag.ESTIMATIVA]) for a in anos}
            for geo, por_ano in sorted(serie.items())
        }
        seg = Segmento(
            id="projecoes2024",
            subindicador="principal",
            rotulo=f"Estimativa IBGE ({anos[0]}–{anos[-1]})",
            fonte="IBGE – Projeções da População, Revisão 2024",
            fonte_url=ibge_projecoes.URL_PUBLICACAO,
            tabela=f"projecoes_2024_tab4_indicadores.xlsx — coluna {self.coluna}",
            extraido_em=carregar_manifest()[ibge_projecoes.ARQUIVO].baixado_em,
            notas=(
                "Estimativa do IBGE, que corrige o sub-registro de óbitos. Até "
                f"{ULTIMO_ANO_TABUA} os valores coincidem com as Tábuas Completas de Mortalidade "
                "publicadas pelo IBGE. Anos mais recentes entram quando a Tábua do ano for "
                "publicada."
            ),
            anos=anos,
            valores=valores,
        )
        return Indicador(
            id=self.id,
            nome=self.nome,
            tema=self.tema,
            unidade=self.unidade,
            unidade_detalhe=self.unidade_detalhe,
            direcao=self.direcao,  # type: ignore[arg-type]
            casas_decimais=self.casas,
            tipo_valor="estimativa",
            subindicadores=[Subindicador(id="principal", nome=self.nome)],
            segmentos=[seg, *self._referencias(fim)],
            escalas={"principal": escala_quantil([seg], self.casas)},
            versao_pipeline=versao_pipeline,
        )

    def _referencias(self, fim: int) -> list[Segmento]:
        """Séries de apoio (papel "referencia"), só no painel. Nenhuma por padrão."""
        return []


class MortInfantil(IndicadorProjecao):
    """Estimativa do IBGE + taxa direta do DATASUS como referência (PROJECT.md, 4.1)."""

    def _referencias(self, fim: int) -> list[Segmento]:
        preliminares = min(SIM.anos_preliminares() + SINASC.anos_preliminares())
        ultimo = min(fim, preliminares - 1)
        anos = list(range(ANO_INICIAL, ultimo + 1))
        valores: dict[str, dict[str, Ponto]] = {}
        extracoes: list[date] = []
        for ano in anos:
            obitos, em1 = SIM.por_uf(ano, {"SFaixa_Etária": [SIM_FAIXA_MENOR_1_ANO]})
            nascidos, em2 = SINASC.por_uf(ano)
            extracoes += [em1, em2]
            for geo, n in obitos.items():
                taxa = n / nascidos[geo] * 1000
                valores.setdefault(geo, {})[str(ano)] = Ponto(v=round(taxa, 2), n=n)
        return [
            Segmento(
                id="datasus_direta",
                subindicador="principal",
                papel="referencia",
                rotulo="Taxa direta DATASUS (referência)",
                fonte="Ministério da Saúde – SIM e SINASC (DATASUS)",
                fonte_url=SIM.url_formulario,
                tabela=(
                    "TabNet obt10uf.def (óbitos p/ residência, faixa etária Menor 1 ano) ÷ "
                    "nvuf.def (nascidos vivos p/ residência da mãe) × 1000"
                ),
                extraido_em=min(extracoes),
                notas=(
                    "Série de referência, calculada diretamente dos registros: óbitos de menores "
                    "de 1 ano no SIM ÷ nascidos vivos no SINASC × 1000. No início dos anos 2000 o "
                    "sub-registro de óbitos, maior no Norte e no Nordeste, faz a taxa direta "
                    "subestimar a mortalidade justamente nos estados mais pobres. Por isso o "
                    "indicador principal é a estimativa do IBGE, que corrige o sub-registro."
                ),
                anos=anos,
                valores=dict(sorted(valores.items())),
            )
        ]


def esperanca_vida() -> IndicadorProjecao:
    return IndicadorProjecao(
        "esperanca_vida",
        "e0_T",
        "Esperança de vida ao nascer",
        "Saúde",
        "anos",
        "anos de vida esperados ao nascer (estimativa IBGE)",
        "maior_melhor",
        1,
        Regras(
            faixa=(40, 90),
            limiar_variacao=0.03,
            metodologias={"projecoes2024": (2000, None)},
        ),
    )


def mort_infantil() -> IndicadorProjecao:
    return MortInfantil(
        "mort_infantil",
        "TMI_T",
        "Taxa de mortalidade infantil",
        "Saúde",
        "por mil nascidos vivos",
        "óbitos de menores de 1 ano por mil nascidos vivos (estimativa IBGE)",
        "menor_melhor",
        1,
        Regras(
            faixa=(0, 150),
            limiar_variacao=0.15,
            metodologias={"projecoes2024": (2000, None), "datasus_direta": (1996, None)},
        ),
    )
