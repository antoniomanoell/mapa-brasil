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


Serie = dict[str, dict[int, float | None]]  # geo → ano → valor


def consultar_categorias(
    tabela: int,
    variaveis: list[int],
    anos: tuple[int, int],
    classificacao: str | None = None,
) -> tuple[dict[int, dict[tuple[str, ...], Serie]], date]:
    """Valores por variável → categorias → geo ("BR" ou UF) → ano, para Brasil e todas as UFs.

    As categorias vêm como tupla de ids, uma por classificação, na ordem em que o SIDRA as devolve.
    """
    vars_ = "|".join(str(v) for v in variaveis)
    params = {"localidades": "N1[all]|N3[all]"}
    if classificacao:
        params["classificacao"] = classificacao
    resp = requisitar(f"{API}/{tabela}/periodos/{anos[0]}-{anos[1]}/variaveis/{vars_}", params)
    saida: dict[int, dict[tuple[str, ...], Serie]] = {}
    for var in json.loads(resp.conteudo):
        por_cat = saida.setdefault(int(var["id"]), {})
        for res in var["resultados"]:
            cats = tuple(next(iter(c["categoria"])) for c in res.get("classificacoes", []))
            por_geo = por_cat.setdefault(cats, {})
            for s in res["series"]:
                loc = s["localidade"]
                geo = BR if loc["nivel"]["id"] == "N1" else str(loc["id"])
                if geo != BR and geo not in CODIGOS_UF:
                    continue
                por_geo[geo] = {
                    int(a): (None if v in SEM_VALOR else float(v)) for a, v in s["serie"].items()
                }
    return saida, resp.obtido_em


def consultar(
    tabela: int,
    variaveis: list[int],
    anos: tuple[int, int],
    classificacao: str | None = None,
) -> tuple[dict[int, Serie], date]:
    """Variável → geo → ano, para consultas com uma única combinação de categorias."""
    dados, obtido_em = consultar_categorias(tabela, variaveis, anos, classificacao)
    saida: dict[int, Serie] = {}
    for var, por_cat in dados.items():
        if len(por_cat) > 1:
            raise ValueError(
                f"SIDRA {tabela}: {len(por_cat)} combinações de categorias; "
                "use consultar_categorias"
            )
        saida[var] = next(iter(por_cat.values()), {})
    return saida, obtido_em


def consultar_areas_mensal(
    tabela: int,
    variavel: int,
    meses: list[str],
    classificacao: str,
) -> tuple[dict[str, dict[str, float | None]], date]:
    """Índices de preços: valor por área (código do SIDRA, "BR" para o Brasil) → mês (AAAAMM).

    As áreas são regiões metropolitanas (N7) e municípios (N6), como o IBGE publica o IPCA e o
    INPC; não há valor por UF.
    """
    params = {"localidades": "N1[all]|N6[all]|N7[all]", "classificacao": classificacao}
    resp = requisitar(f"{API}/{tabela}/periodos/{'|'.join(meses)}/variaveis/{variavel}", params)
    saida: dict[str, dict[str, float | None]] = {}
    for var in json.loads(resp.conteudo):
        for res in var["resultados"]:
            for s in res["series"]:
                loc = s["localidade"]
                geo = BR if loc["nivel"]["id"] == "N1" else str(loc["id"])
                serie = saida.setdefault(geo, {})
                for mes, v in s["serie"].items():
                    serie[mes] = None if v in SEM_VALOR else float(v)
    return saida, resp.obtido_em
