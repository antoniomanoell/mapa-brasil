"""Série única de população por UF (PROJECT.md, 4.2): Projeções do IBGE, Revisão 2024."""

from .sources import ibge_projecoes

FONTE = "IBGE – Projeções da População, Revisão 2024"


def populacao(ate_ano: int) -> dict[str, dict[int, float]]:
    """População total por geografia ("BR" ou código da UF) e ano, até `ate_ano`."""
    return ibge_projecoes.serie("POP_T", ate_ano)
