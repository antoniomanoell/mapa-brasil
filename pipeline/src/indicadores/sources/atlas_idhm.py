"""PNUD/IPEA/FJP — Atlas Brasil: IDHM censitário (2000, 2010) e Radar IDHM (PNADC)."""

from functools import cache

import openpyxl

from ..raw_manual import exigir
from ..ufs import BR, CODIGOS_UF

ARQUIVO_CENSO = "atlas_idhm/censo_total_1991_2010.xlsx"
ARQUIVO_RADAR = "atlas_idhm/adh_radar_base_2012_2024.xlsx"
URL_BIBLIOTECA = "https://www.atlasbrasil.org.br/acervo/biblioteca"

# Colunas de cada dimensão, iguais nas duas bases.
COLUNAS = {"geral": "IDHM", "longevidade": "IDHM_L", "educacao": "IDHM_E", "renda": "IDHM_R"}

Serie = dict[str, dict[str, dict[int, float]]]  # dimensão → geo → ano → valor


def _tabela(arquivo: str, aba: str) -> list[dict[str, object]]:
    wb = openpyxl.load_workbook(exigir(arquivo), read_only=True, data_only=True)
    it = wb[aba].iter_rows(values_only=True)
    cab = [str(c).strip() if c is not None else "" for c in next(it)]
    return [dict(zip(cab, linha, strict=False)) for linha in it if any(linha)]


def _acumular(saida: Serie, geo: str, ano: int, linha: dict[str, object]) -> None:
    for dim, col in COLUNAS.items():
        valor = linha[col]
        if valor is None:
            raise ValueError(f"Atlas Brasil: {col} vazio em {geo}/{ano}")
        saida.setdefault(dim, {}).setdefault(geo, {})[ano] = float(valor)  # type: ignore[arg-type]


@cache
def censo(anos: tuple[int, ...] = (2000, 2010)) -> Serie:
    saida: Serie = {}
    for linha in _tabela(ARQUIVO_CENSO, "UF 91-00-10"):
        ano, geo = int(linha["ANO"]), str(linha["UF"])  # type: ignore[call-overload]
        if ano in anos and geo in CODIGOS_UF:
            _acumular(saida, geo, ano, linha)
    for linha in _tabela(ARQUIVO_CENSO, "BR 91-00-10"):
        ano = int(linha["ANO"])  # type: ignore[call-overload]
        if ano in anos:
            _acumular(saida, BR, ano, linha)
    return saida


@cache
def radar() -> Serie:
    saida: Serie = {}
    for linha in _tabela(ARQUIVO_RADAR, "Total"):
        ano = int(linha["ANO"])  # type: ignore[call-overload]
        if linha["AGREGACAO"] == "Brasil":
            _acumular(saida, BR, ano, linha)
        elif linha["AGREGACAO"] == "Unidade da Federação":
            _acumular(saida, str(linha["CODIGO"]), ano, linha)
    return saida
