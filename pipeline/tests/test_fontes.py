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
