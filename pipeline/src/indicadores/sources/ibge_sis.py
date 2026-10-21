"""IBGE — Síntese de Indicadores Sociais 2025: Tabela 2.23 (pobreza e extrema pobreza por UF).

Uma aba por ano (2012–2024) e outra com os CVs ("AAAA (CV)"). As colunas são achadas pelo texto do
cabeçalho, e as linhas pelo nome da UF (a primeira ocorrência: a capital de mesmo nome vem depois).
"""

import re
import zipfile
from dataclasses import dataclass
from functools import cache

import xlrd

from ..raw_manual import exigir
from ..ufs import BR, UFS

ARQUIVO = "ibge_sis/sis2025_2_Distribuicao_Renda_xls.zip"
TABELA = "Tabela 2.23"
URL = (
    "https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/"
    "Sintese_de_Indicadores_Sociais_2025/Tabelas/xls/"
)
_NOMES = {"Brasil": BR, **{uf.nome: uf.codigo for uf in UFS}}


@dataclass(frozen=True)
class Proporcao:
    v: float
    cv: float | None


@dataclass(frozen=True)
class Pobreza:
    # linha ("US$ 2,15 PPC 2017") → geo → ano → proporção (%)
    valores: dict[str, dict[str, dict[int, Proporcao]]]
    # ano → texto da fonte da aba (diz se foram primeiras ou quintas visitas)
    fontes: dict[int, str]


def _colunas(sh: xlrd.sheet.Sheet) -> dict[str, int]:
    """Linha de pobreza → índice da coluna "Proporção de pessoas ... menor que US$ X PPC 2017"."""
    saida = {}
    for r in range(min(8, sh.nrows)):
        for c, texto in enumerate(sh.row_values(r)):
            m = re.search(r"Proporção de pessoas.*menor que (US\$ [\d,]+ PPC \d{4})", str(texto))
            if m:
                saida[m.group(1)] = c
    if not saida:
        raise ValueError(f"{TABELA}, aba {sh.name}: colunas de proporção não encontradas")
    return saida


def _ler_aba(sh: xlrd.sheet.Sheet) -> tuple[dict[str, dict[str, float]], str]:
    colunas = _colunas(sh)
    por_linha: dict[str, dict[str, float]] = {linha: {} for linha in colunas}
    fonte = ""
    for r in range(sh.nrows):
        nome = str(sh.cell_value(r, 0)).strip()
        if nome.startswith("Fonte"):
            fonte = nome
        geo = _NOMES.get(nome)
        if geo is None:
            continue
        for linha, c in colunas.items():
            if geo in por_linha[linha]:
                continue  # capital homônima (Rio de Janeiro, São Paulo) vem depois da UF
            v = sh.cell_value(r, c)
            if isinstance(v, float):
                por_linha[linha][geo] = v
    return por_linha, fonte


@cache
def tabela_2_23() -> Pobreza:
    zf = zipfile.ZipFile(exigir(ARQUIVO))
    nome = next(n for n in zf.namelist() if TABELA in n)
    wb = xlrd.open_workbook(file_contents=zf.read(nome))
    valores: dict[str, dict[str, dict[int, Proporcao]]] = {}
    fontes: dict[int, str] = {}
    for aba in wb.sheet_names():
        if not re.fullmatch(r"\d{4}", aba):
            continue
        ano = int(aba)
        props, fonte = _ler_aba(wb.sheet_by_name(aba))
        cvs, _ = _ler_aba(wb.sheet_by_name(f"{aba} (CV)"))
        fontes[ano] = fonte
        for linha, por_geo in props.items():
            for geo, v in por_geo.items():
                alvo = valores.setdefault(linha, {}).setdefault(geo, {})
                alvo[ano] = Proporcao(v=v, cv=cvs.get(linha, {}).get(geo))
    for linha, por_geo in valores.items():
        faltando = set(_NOMES.values()) - set(por_geo)
        if faltando:
            raise ValueError(f"{TABELA}, {linha}: geografias ausentes {sorted(faltando)}")
    return Pobreza(valores=valores, fontes=fontes)
