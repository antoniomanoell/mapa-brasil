"""IBGE — Contas Regionais (referência 2010), tabelas especiais 2002–2023.

tab01: PIB a preços correntes (R$ milhões). tab03: série encadeada do volume do PIB (2002 = 100).
Linhas achadas pelo nome (Brasil e UFs; as grandes regiões são ignoradas), anos pelo cabeçalho.
"""

import zipfile
from dataclasses import dataclass
from functools import cache

import xlrd

from ..raw_manual import exigir
from ..ufs import BR, UFS

ARQUIVO = "ibge_contas_regionais/Especiais_2002_2023_xls.zip"
URL = "https://ftp.ibge.gov.br/Contas_Regionais/2023/xls/"
_NOMES = {"Brasil": BR, **{uf.nome: uf.codigo for uf in UFS}}

Serie = dict[str, dict[int, float]]  # geo → ano → valor


@dataclass(frozen=True)
class ContasRegionais:
    pib_corrente: Serie  # R$ milhões
    volume: Serie  # índice encadeado, 2002 = 100


def ler_tabela(sh: xlrd.sheet.Sheet) -> Serie:
    """Acha a linha de anos no cabeçalho e lê Brasil e as 27 UFs."""
    linha_anos = next(
        r
        for r in range(min(10, sh.nrows))
        if sum(isinstance(c, float) and 1990 < c < 2100 for c in sh.row_values(r)) > 5
    )
    anos = {c: int(v) for c, v in enumerate(sh.row_values(linha_anos)) if isinstance(v, float)}
    saida: Serie = {}
    for r in range(linha_anos + 1, sh.nrows):
        geo = _NOMES.get(str(sh.cell_value(r, 0)).strip())
        if geo is None or geo in saida:
            continue
        saida[geo] = {
            ano: float(sh.cell_value(r, c))
            for c, ano in anos.items()
            if isinstance(sh.cell_value(r, c), float)
        }
    faltando = set(_NOMES.values()) - set(saida)
    if faltando:
        raise ValueError(f"Contas Regionais, {sh.name}: geografias ausentes {sorted(faltando)}")
    return saida


@cache
def especiais() -> ContasRegionais:
    zf = zipfile.ZipFile(exigir(ARQUIVO))

    def aba(nome: str) -> xlrd.sheet.Sheet:
        return xlrd.open_workbook(file_contents=zf.read(nome)).sheet_by_index(0)

    return ContasRegionais(
        pib_corrente=ler_tabela(aba("tab01.xls")), volume=ler_tabela(aba("tab03.xls"))
    )
