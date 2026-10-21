"""Índices de preços do IBGE (SIDRA) para deflacionar valores monetários (PROJECT.md, 2.5)."""

import json
import statistics
from datetime import date

from .sources.http import requisitar
from .sources.ibge_sidra import API, SEM_VALOR, url_tabela

# Número-índice mensal (base dez/1993 = 100), Brasil.
IPCA = (1737, 2266)
INPC = (1736, 2289)


def indice_mensal(indice: tuple[int, int], inicio: int, fim: int) -> tuple[dict[str, float], date]:
    """Mês ("AAAAMM") → número-índice, de janeiro de `inicio` a dezembro de `fim`."""
    tabela, variavel = indice
    resp = requisitar(
        f"{API}/{tabela}/periodos/{inicio}01-{fim}12/variaveis/{variavel}",
        {"localidades": "N1[all]"},
    )
    serie = json.loads(resp.conteudo)[0]["resultados"][0]["series"][0]["serie"]
    valores = {mes: float(v) for mes, v in serie.items() if v not in SEM_VALOR}
    faltando = [
        f"{a}{m:02d}"
        for a in range(inicio, fim + 1)
        for m in range(1, 13)
        if f"{a}{m:02d}" not in valores
    ]
    if faltando:
        raise ValueError(f"{url_tabela(tabela)}: sem número-índice para {faltando}")
    return valores, resp.obtido_em


def media_anual(indices: dict[str, float], ano: int) -> float:
    return statistics.fmean(indices[f"{ano}{m:02d}"] for m in range(1, 13))
