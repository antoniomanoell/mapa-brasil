"""Cálculo da renda per capita da PNAD em microdados sintéticos (os reais não vão para o git)."""

import polars as pl
import pytest

from indicadores.sources import ibge_pnad_microdados as pnad
from indicadores.ufs import BR, CODIGOS_UF


def test_le_layout_do_input_sas():
    texto = """
        INPUT  @00001  V0101  $4.    /* ANO */
               @00005  V0102  $8.    /* CONTROLE */
               @00094  V4605   12.10 /* PROBABILIDADE */
               @00162  STRAT   7.    /* V4617 */
    """
    assert pnad.ler_layout(texto) == {
        "V0101": (1, 4),
        "V0102": (5, 8),
        "V4605": (94, 12),
        "STRAT": (162, 7),
    }


def _dados(extra_dom=(), extra_pes=()):
    """Um domicílio por UF, duas UPAs por estrato, para todas as geos terem casos."""
    dom, pes = [], []
    for i, uf in enumerate(sorted(CODIGOS_UF)):
        for j, (renda, condicoes) in enumerate([("1000", "13"), ("0", "1"), ("3000", "126")]):
            ctrl = f"{uf}{i:02d}{j:04d}"
            dom.append(
                {
                    "V0102": ctrl,
                    "V0103": "001",
                    "V0201": "1",
                    "V4611": "100",
                    "V4614": renda,
                    "V4617": f"{uf}01",
                    "V4618": str(j % 2),
                }
            )
            pes += [{"V0102": ctrl, "V0103": "001", "V0401": c, "V4729": "100"} for c in condicoes]
    dom += list(extra_dom)
    pes += list(extra_pes)
    return pl.DataFrame(dom), pl.DataFrame(pes)


def test_conceito_por_pessoa_e_conceito_sis():
    dom, pes = _dados()
    por_pessoa, sis = pnad.calcular(dom, pes)
    # Per capita: 1000/2, 0/1 e 3000/2 (o empregado doméstico, condição 6, não conta).
    # Por pessoa, com o sem rendimento: (500·2 + 0·1 + 1500·2) / 5 = 800.
    assert por_pessoa["28"].media == pytest.approx(800)
    assert por_pessoa[BR].media == pytest.approx(800)
    # Conceito da SIS: por domicílio e sem o domicílio sem rendimento: (500 + 1500) / 2.
    assert sis["28"].media == pytest.approx(1000)
    assert por_pessoa["28"].cv is not None and por_pessoa["28"].cv > 0


def test_exclui_sem_declaracao_e_domicilio_coletivo():
    extra_dom = [
        {
            "V0102": "35990001",
            "V0103": "001",
            "V0201": "1",
            "V4611": "100",
            "V4614": str(pnad.SEM_DECLARACAO),
            "V4617": "3501",
            "V4618": "0",
        },
        {
            "V0102": "35990002",
            "V0103": "001",
            "V0201": "5",
            "V4611": "100",
            "V4614": "90000",
            "V4617": "3501",
            "V4618": "1",
        },
    ]
    extra_pes = [
        {"V0102": c, "V0103": "001", "V0401": "1", "V4729": "100"} for c in ("35990001", "35990002")
    ]
    dom, pes = _dados(extra_dom, extra_pes)
    por_pessoa, _ = pnad.calcular(dom, pes)
    assert por_pessoa["35"].media == pytest.approx(800)


def test_confere_per_capita_publicado():
    dom, pes = _dados()
    dom = dom.with_columns(pl.lit("1").alias("V4621"))
    with pytest.raises(ValueError, match="V4621"):
        pnad.calcular(dom, pes)


def test_cv_por_linearizacao():
    # Dois estratos com duas UPAs, peso 1: a variância da média é a da amostragem com reposição.
    casos = pl.DataFrame(
        {
            "rpc": [10.0, 20.0, 30.0, 40.0],
            "peso": [1.0] * 4,
            "V4617": ["a", "a", "b", "b"],
            "upa": ["a1", "a2", "b1", "b2"],
        }
    )
    est = pnad._media_com_cv(casos, "rpc", "peso", casos.select("V4617", "upa"))
    # z = (y - 25)/4 → (-3.75, -1.25 | 1.25, 3.75); cada estrato: 2/1 · (2·1.25²) = 6.25.
    assert est.media == pytest.approx(25)
    assert est.cv == pytest.approx((2 * 6.25) ** 0.5 / 25 * 100)


def test_gini_ponderado():
    import polars as pl

    g = pnad.gini_ponderado
    assert g(pl.Series([5.0, 5.0, 5.0]), pl.Series([1.0, 2.0, 3.0])) == pytest.approx(0.0)
    assert g(pl.Series([0.0, 0.0, 0.0, 1.0]), pl.Series([1.0] * 4)) == pytest.approx(0.75)
    # Peso 2 equivale a repetir o caso.
    assert g(pl.Series([1.0, 3.0]), pl.Series([2.0, 1.0])) == pytest.approx(
        g(pl.Series([1.0, 1.0, 3.0]), pl.Series([1.0, 1.0, 1.0]))
    )


def test_analfabetismo_15_ou_mais_entre_quem_respondeu():
    dom, _ = _dados()
    # Em cada UF: duas pessoas de 15+ que sabem ler, uma que não sabe, uma criança que não sabe
    # (fora da idade) e uma sem resposta (fora do universo). Peso 100 para todos.
    linhas = []
    for ctrl in dom["V0102"].to_list():
        for idade, leitura in [("30", "1"), ("40", "1"), ("70", "3"), ("08", "3"), ("50", "")]:
            linhas.append(
                {"V0102": ctrl, "V0103": "001", "V8005": idade, "V0601": leitura, "V4729": "100"}
            )
    taxa = pnad.calcular_analfabetismo(dom, pl.DataFrame(linhas))
    assert taxa["28"].media == pytest.approx(100 / 3)
    assert taxa[BR].media == pytest.approx(100 / 3)
