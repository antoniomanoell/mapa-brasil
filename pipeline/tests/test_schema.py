import pytest
from pydantic import ValidationError

from indicadores.schema import Ponto
from tests.conftest import indicador, segmento


def test_lacuna_exige_motivo():
    with pytest.raises(ValidationError):
        Ponto(v=None)
    assert Ponto(v=None, lacuna="sem pesquisa").v is None


def test_valor_com_lacuna_e_invalido():
    with pytest.raises(ValidationError):
        Ponto(v=1.0, lacuna="x")


def test_anos_fora_da_lista_declarada():
    seg = segmento("a", [2001, 2002])
    with pytest.raises(ValidationError, match="anos fora"):
        segmento("a", [2001], valores=seg.valores)


def test_geo_invalida():
    seg = segmento("a", [2001])
    with pytest.raises(ValidationError):
        segmento("a", [2001], valores={**seg.valores, "SE": seg.valores["28"]})


def test_subindicador_inexistente():
    seg = segmento("a", [2001, 2002, 2003])
    with pytest.raises(ValidationError, match="inexistente"):
        indicador([seg.model_copy(update={"subindicador": "outro"})])


def test_roundtrip_json():
    ind = indicador([segmento("a", [2001, 2002, 2003])])
    texto = ind.model_dump_json(exclude_defaults=True)
    assert type(ind).model_validate_json(texto) == ind
