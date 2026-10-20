"""IBGE — Projeções da População, Revisão 2024: tabela 4 (indicadores implícitos)."""

from functools import cache

import openpyxl

from ..raw_manual import exigir
from ..ufs import BR, CODIGOS_UF, GEOS_OBRIGATORIAS

ARQUIVO = "ibge_projecoes/projecoes_2024_tab4_indicadores.xlsx"
ABA = "4) INDICADORES"
URL_PUBLICACAO = "https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2024/"


@cache
def _linhas() -> tuple[dict[str, object], ...]:
    wb = openpyxl.load_workbook(exigir(ARQUIVO), read_only=True, data_only=True)
    it = wb[ABA].iter_rows(values_only=True)
    for cabecalho in it:
        if cabecalho and cabecalho[0] == "ANO":
            break
    else:
        raise ValueError(f"{ARQUIVO}: cabeçalho 'ANO' não encontrado — formato mudou?")
    nomes = [str(c) if c is not None else "" for c in cabecalho]
    return tuple(dict(zip(nomes, linha, strict=False)) for linha in it if linha and linha[0])


def _geo(codigo: object) -> str | None:
    """CÓD. 0 = Brasil; 11–53 = UFs; 1–5 = grandes regiões (ignoradas)."""
    cod = int(codigo)  # type: ignore[call-overload]
    if cod == 0:
        return BR
    texto = str(cod)
    return texto if texto in CODIGOS_UF else None


def serie(coluna: str, ate_ano: int) -> dict[str, dict[int, float]]:
    """Valores de `coluna` por geografia e ano, de 2000 até `ate_ano` (corta a projeção)."""
    saida: dict[str, dict[int, float]] = {}
    for linha in _linhas():
        geo = _geo(linha["CÓD."])
        ano = int(linha["ANO"])  # type: ignore[call-overload]
        if geo is None or ano > ate_ano:
            continue
        valor = linha[coluna]
        if valor is None:
            raise ValueError(f"{ARQUIVO}: {coluna} vazio para {geo}/{ano}")
        saida.setdefault(geo, {})[ano] = float(valor)  # type: ignore[arg-type]
    faltando = GEOS_OBRIGATORIAS - set(saida)
    if faltando:
        raise ValueError(f"{ARQUIVO}: geografias ausentes: {sorted(faltando)}")
    return saida
