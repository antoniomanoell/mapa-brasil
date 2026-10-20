from indicadores.schema import Flag, Ponto
from indicadores.validate import Referencia, validar
from tests.conftest import HOJE, indicador, refs_validas, segmento


def _trocar_ponto(seg, geo, ano, ponto):
    valores = {g: dict(s) for g, s in seg.valores.items()}
    valores[geo][str(ano)] = ponto
    return seg.model_copy(update={"valores": valores})


def test_indicador_valido_passa(regras):
    ind = indicador([segmento("a", [2001, 2002, 2003]), segmento("b", [2012, 2013])])
    res = validar(ind, regras, refs_validas(ind), HOJE)
    assert res.ok, res.erros
    assert len(res.conferencias) == 3


def test_cobertura_falta_uf(regras):
    seg = segmento("a", [2001, 2002, 2003])
    valores = {g: s for g, s in seg.valores.items() if g != "14"}
    ind = indicador([seg.model_copy(update={"valores": valores})])
    res = validar(ind, regras, refs_validas(ind), HOJE)
    assert any("14 sem valor" in e for e in res.erros)


def test_lacuna_explicita_conta_como_cobertura(regras):
    seg = _trocar_ponto(segmento("a", [2001, 2002, 2003]), "14", 2002, Ponto(v=None, lacuna="x"))
    ind = indicador([seg])
    assert validar(ind, regras, refs_validas(ind), HOJE).ok


def test_faixa_plausivel(regras):
    seg = _trocar_ponto(segmento("a", [2001, 2002, 2003]), "14", 2002, Ponto(v=150.0))
    res = validar(indicador([seg]), regras, [], HOJE)
    assert any("fora da faixa" in e for e in res.erros)


def test_preliminar_proibido(regras):
    seg = _trocar_ponto(
        segmento("a", [2001, 2002, 2003]), "14", 2002, Ponto(v=10.0, flags=[Flag.PRELIMINAR])
    )
    res = validar(indicador([seg]), regras, [], HOJE)
    assert any("preliminar" in e for e in res.erros)


def test_cv_alto_exige_flag(regras):
    seg = _trocar_ponto(segmento("a", [2001, 2002, 2003]), "14", 2002, Ponto(v=10.0, cv=20.0))
    res = validar(indicador([seg]), regras, [], HOJE)
    assert any("baixa_precisao" in e for e in res.erros)


def test_sem_projecoes(regras):
    ind = indicador([segmento("b", [2024, 2025, 2026])])
    res = validar(ind, regras, refs_validas(ind), HOJE)
    assert any("projeção" in e and "2026" in e for e in res.erros)


def test_sem_emenda(regras):
    ind = indicador([segmento("a", [2014, 2015, 2016])])
    res = validar(ind, regras, refs_validas(ind), HOJE)
    assert any("fora do intervalo da metodologia" in e for e in res.erros)


def test_metodologia_nao_declarada(regras):
    ind = indicador([segmento("x", [2001, 2002, 2003])])
    res = validar(ind, regras, refs_validas(ind), HOJE)
    assert any("não declarada" in e for e in res.erros)


def test_variacao_suspeita_e_alerta_nao_erro(regras):
    seg = _trocar_ponto(segmento("a", [2001, 2002, 2003]), "14", 2002, Ponto(v=90.0))
    ind = indicador([seg])
    res = validar(ind, regras, refs_validas(ind), HOJE)
    assert res.ok
    assert any("14: 2001→2002" in a for a in res.alertas)


def test_conferencia_minimo_e_br_recente(regras):
    ind = indicador([segmento("a", [2001, 2002, 2003])])
    res = validar(ind, regras, refs_validas(ind)[1:], HOJE)
    assert any("mínimo 3" in e for e in res.erros)
    assert any("Brasil no ano mais recente" in e for e in res.erros)


def test_conferencia_divergente(regras):
    ind = indicador([segmento("a", [2001, 2002, 2003])])
    refs = refs_validas(ind)
    r0 = refs[0]
    errada = Referencia(**{**r0.__dict__, "valor": r0.valor + 1})
    res = validar(ind, regras, [errada, *refs[1:]], HOJE)
    assert any("≠ publicado" in e for e in res.erros)
