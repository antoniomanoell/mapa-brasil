"""IBGE — API de agregados do SIDRA (servicodados.ibge.gov.br/api/v3/agregados)."""

import json
from datetime import date

from ..ufs import BR, CODIGOS_UF
from .http import baixar_json, requisitar

API = "https://servicodados.ibge.gov.br/api/v3/agregados"
# Símbolos do SIDRA para valor inexistente ou sigiloso.
SEM_VALOR = {"-", "..", "...", "X", ""}


def url_tabela(tabela: int) -> str:
    return f"https://sidra.ibge.gov.br/tabela/{tabela}"


def periodo(tabela: int) -> tuple[int, int]:
    """(ano inicial, ano final) declarados nos metadados da tabela."""
    meta = baixar_json(f"{API}/{tabela}/metadados", usar_cache=False)
    per = meta["periodicidade"]
    return int(per["inicio"]), int(per["fim"])


def consultar(
    tabela: int,
    variaveis: list[int],
    anos: tuple[int, int],
    classificacao: str | None = None,
) -> tuple[dict[int, dict[str, dict[int, float | None]]], date]:
    """Valores por variável → geo ("BR" ou UF) → ano, para Brasil e todas as UFs."""
    vars_ = "|".join(str(v) for v in variaveis)
    params = {"localidades": "N1[all]|N3[all]"}
    if classificacao:
        params["classificacao"] = classificacao
    resp = requisitar(f"{API}/{tabela}/periodos/{anos[0]}-{anos[1]}/variaveis/{vars_}", params)
    saida: dict[int, dict[str, dict[int, float | None]]] = {}
    for var in json.loads(resp.conteudo):
        por_geo = saida.setdefault(int(var["id"]), {})
        for res in var["resultados"]:
            for s in res["series"]:
                loc = s["localidade"]
                geo = BR if loc["nivel"]["id"] == "N1" else str(loc["id"])
                if geo != BR and geo not in CODIGOS_UF:
                    continue
                por_geo[geo] = {
                    int(a): (None if v in SEM_VALOR else float(v)) for a, v in s["serie"].items()
                }
    return saida, resp.obtido_em
