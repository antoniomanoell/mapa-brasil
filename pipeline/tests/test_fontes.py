"""Testes de parsing das fontes, sem rede (respostas gravadas em miniatura)."""

import json
from datetime import date

import pytest

from indicadores.sources import datasus_tabnet, ibge_sidra
from indicadores.sources.http import Resposta
from indicadores.ufs import BR, CODIGOS_UF


def _prn(linhas: list[str]) -> str:
    corpo = "\n".join(['"Unidade da Federação";"Óbitos p/Residênc"', *linhas, '"Total";99', "&"])
    return f"<html><PRE>\n{corpo}\n</PRE></html>"


def test_tabnet_le_ufs_total_e_zero():
    linhas = [f'"{c} UF {c}";{"-" if c == "14" else "3"}' for c in sorted(CODIGOS_UF)]
    linhas.append('"Ignorado/exterior";2')
    saida = datasus_tabnet.ler_prn(_prn(linhas), "teste")
    assert saida[BR] == 99
    assert saida["14"] == 0
    assert saida["35"] == 3
    assert "Ignorado/exterior" not in saida


def test_tabnet_falta_uf():
    linhas = [f'"{c} UF";1' for c in sorted(CODIGOS_UF) if c != "53"]
    with pytest.raises(ValueError, match="53"):
        datasus_tabnet.ler_prn(_prn(linhas), "teste")


def test_sidra_le_brasil_ufs_e_simbolos(monkeypatch):
    def serie(geo_id, nivel, valores):
        return {"localidade": {"id": geo_id, "nivel": {"id": nivel}}, "serie": valores}

    resposta = [
        {
            "id": "10816",
            "resultados": [
                {
                    "series": [
                        serie("1", "N1", {"2024": "2118", "2025": "2264"}),
                        serie("28", "N3", {"2024": "1494", "2025": "..."}),
                    ]
                }
            ],
        }
    ]
    monkeypatch.setattr(
        ibge_sidra,
        "requisitar",
        lambda *a, **k: Resposta(json.dumps(resposta).encode(), date.today()),
    )
    dados, _ = ibge_sidra.consultar(7533, [10816], (2024, 2025))
    assert dados[10816][BR] == {2024: 2118.0, 2025: 2264.0}
    assert dados[10816]["28"] == {2024: 1494.0, 2025: None}


class _AbaFalsa:
    """Imita xlrd.sheet.Sheet: só o que ibge_sis usa."""

    def __init__(self, nome, linhas):
        self.name = nome
        self._l = linhas
        self.nrows = len(linhas)

    def row_values(self, r):
        return self._l[r]

    def cell_value(self, r, c):
        return self._l[r][c] if c < len(self._l[r]) else ""


def test_sis_pega_a_uf_e_nao_a_capital_homonima():
    from indicadores.sources import ibge_sis

    cab = [
        "UF",
        "Total",
        "Linha",
        "Proporção de pessoas com rendimento menor que US$ 2,15 PPC 2017",
    ]
    aba = _AbaFalsa(
        "2024",
        [
            cab,
            ["Brasil", 1.0, 2.0, 3.5],
            ["Rio de Janeiro", 1.0, 2.0, 1.8],  # UF
            ["Rio de Janeiro", 1.0, 2.0, 9.9],  # capital, vem depois
            ["Fonte: IBGE, ... acumulado de quintas visitas.", "", "", ""],
        ],
    )
    valores, fonte = ibge_sis._ler_aba(aba)
    assert valores["US$ 2,15 PPC 2017"] == {"BR": 3.5, "33": 1.8}
    assert "quintas" in fonte
