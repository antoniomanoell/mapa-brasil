import pytest

from indicadores.build import item_catalogo
from indicadores.escala import escala_quantil
from indicadores.report import _faixas
from indicadores.sources.ibge_malhas import conferir
from indicadores.ufs import CODIGOS_UF
from tests.conftest import indicador, segmento


def test_escala_ignora_br_e_tem_4_limites():
    seg = segmento("a", [2001, 2002, 2003])
    esc = escala_quantil([seg], 1)
    assert len(esc.limites) == 4
    assert esc.limites == sorted(esc.limites)


def test_faixas_de_anos():
    assert _faixas([2001, 2002, 2003, 2005, 2007, 2008]) == "2001–2003, 2005, 2007–2008"
    assert _faixas([]) == "—"


def test_item_catalogo_anos():
    ind = indicador([segmento("a", [2001, 2002, 2003]), segmento("b", [2012, 2013])])
    item = item_catalogo(ind)
    assert (item.ano_inicial, item.ano_final) == (2001, 2013)


def _topo(codigos):
    geoms = [{"type": "Polygon", "arcs": [], "properties": {"codarea": c}} for c in codigos]
    return {"type": "Topology", "objects": {"BRUF": {"geometries": geoms}}}


def test_malha_confere_27_ufs():
    conferir(_topo(CODIGOS_UF))
    with pytest.raises(ValueError, match="inesperados"):
        conferir(_topo(set(CODIGOS_UF) - {"53"}))
