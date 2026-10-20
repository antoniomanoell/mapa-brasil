"""`idhm` — IDHM geral e dimensões; segmentos Censo e PNADC (ver DECISIONS.md)."""

from datetime import date

from ..escala import escala_quantil
from ..raw_manual import carregar_manifest
from ..schema import Indicador, Ponto, Quebra, Segmento, Subindicador
from ..sources import atlas_idhm
from ..validate import Regras, ultimo_ano_transcorrido

CASAS = 3
SUBINDICADORES = [
    Subindicador(id="geral", nome="IDHM"),
    Subindicador(id="longevidade", nome="IDHM Longevidade"),
    Subindicador(id="educacao", nome="IDHM Educação"),
    Subindicador(id="renda", nome="IDHM Renda"),
]
FONTE = "PNUD, Ipea e FJP – Atlas do Desenvolvimento Humano no Brasil"


def _segmento(
    id_: str, sub: str, serie: dict[str, dict[int, float]], ate: int, arquivo: str, **kw: str
) -> Segmento:
    anos = sorted({a for por_ano in serie.values() for a in por_ano if a <= ate})
    valores = {
        geo: {str(a): Ponto(v=por_ano[a]) for a in anos if a in por_ano}
        for geo, por_ano in sorted(serie.items())
    }
    return Segmento(
        id=id_,
        subindicador=sub,
        fonte=FONTE,
        fonte_url=atlas_idhm.URL_BIBLIOTECA,
        extraido_em=carregar_manifest()[arquivo].baixado_em,
        anos=anos,
        valores=valores,
        **kw,  # type: ignore[arg-type]
    )


class Idhm:
    id = "idhm"
    regras = Regras(
        faixa=(0, 1),
        limiar_variacao=0.08,
        metodologias={"censo": (1991, 2010), "pnadc": (2012, None)},
    )

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        ate = ultimo_ano_transcorrido(hoje)
        censo, radar = atlas_idhm.censo(), atlas_idhm.radar()
        segmentos: list[Segmento] = []
        for sub in SUBINDICADORES:
            segmentos.append(
                _segmento(
                    "censo",
                    sub.id,
                    censo[sub.id],
                    ate,
                    atlas_idhm.ARQUIVO_CENSO,
                    rotulo="Censo (2000, 2010)",
                    tabela="censo_total_1991_2010.xlsx — abas 'UF 91-00-10' e 'BR 91-00-10'",
                    notas=(
                        "Calculado com os Censos Demográficos de 2000 e 2010, que só existem a "
                        "cada dez anos: não há valores nos anos intermediários."
                    ),
                )
            )
            segmentos.append(
                _segmento(
                    "pnadc",
                    sub.id,
                    radar[sub.id],
                    ate,
                    atlas_idhm.ARQUIVO_RADAR,
                    rotulo="Radar IDHM – PNAD Contínua (2012–)",
                    tabela="adh_radar_base_2012_2024.xlsx — aba 'Total'",
                    notas=(
                        "Radar IDHM, calculado com a PNAD Contínua. Em 2020 e 2021 foram usados "
                        "os dados da 5ª visita da pesquisa; nos demais anos, os da 1ª visita."
                    ),
                )
            )
        return Indicador(
            id=self.id,
            nome="Índice de Desenvolvimento Humano Municipal (IDHM)",
            tema="Desenvolvimento humano",
            unidade="índice",
            unidade_detalhe="índice de 0 a 1",
            direcao="maior_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=SUBINDICADORES,
            segmentos=segmentos,
            quebras=[
                Quebra(
                    ano=2012,
                    texto=(
                        "Mudança de fonte: Censo Demográfico → PNAD Contínua (Radar IDHM). "
                        "As duas séries não são diretamente comparáveis."
                    ),
                )
            ],
            escalas={
                sub.id: escala_quantil([s for s in segmentos if s.subindicador == sub.id], CASAS)
                for sub in SUBINDICADORES
            },
            versao_pipeline=versao_pipeline,
        )
