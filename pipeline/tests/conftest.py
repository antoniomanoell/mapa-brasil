from datetime import date

import pytest

from indicadores.escala import escala_quantil
from indicadores.schema import Indicador, Ponto, Segmento, Subindicador
from indicadores.ufs import GEOS_OBRIGATORIAS
from indicadores.validate import Referencia, Regras

HOJE = date(2026, 10, 20)


def segmento(id_: str, anos: list[int], base: float = 10.0, **kw) -> Segmento:
    valores = kw.pop("valores", None) or {
        geo: {str(a): Ponto(v=base + i + (a - anos[0]) * 0.1) for a in anos}
        for i, geo in enumerate(sorted(GEOS_OBRIGATORIAS))
    }
    return Segmento(
        id=id_,
        subindicador="principal",
        rotulo=id_.upper(),
        fonte="Teste",
        fonte_url="https://exemplo.gov.br",
        tabela="0000",
        extraido_em=HOJE,
        anos=anos,
        valores=valores,
        **kw,
    )


def indicador(segmentos: list[Segmento], **kw) -> Indicador:
    base = dict(
        id="teste",
        nome="Teste",
        tema="Teste",
        unidade="%",
        unidade_detalhe="%",
        direcao="menor_melhor",
        casas_decimais=1,
        tipo_valor="medido",
        subindicadores=[Subindicador(id="principal", nome="Teste")],
        segmentos=segmentos,
        escalas={"principal": escala_quantil(segmentos, 1)},
        versao_pipeline="abc1234",
    )
    base.update(kw)
    return Indicador(**base)


def refs_validas(ind: Indicador) -> list[Referencia]:
    """Três referências que batem com o próprio indicador (inclui BR no ano mais recente)."""
    seg = ind.segmentos[-1]
    ultimo = seg.anos[-1]
    pontos = [("BR", ultimo), ("28", ultimo), ("35", seg.anos[0])]
    return [
        Referencia(
            indicador=ind.id,
            subindicador=seg.subindicador,
            segmento=seg.id,
            geo=geo,
            ano=ano,
            valor=seg.valores[geo][str(ano)].v,  # type: ignore[arg-type]
            url="https://exemplo.gov.br",
        )
        for geo, ano in pontos
    ]


@pytest.fixture
def regras() -> Regras:
    return Regras(
        faixa=(0, 100), limiar_variacao=0.5, metodologias={"a": (2001, 2015), "b": (2012, None)}
    )
