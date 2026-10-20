"""Escala de cor fixa no tempo (PROJECT.md, 9.2): quantis sobre todos os anos e segmentos."""

import statistics

from .schema import Escala, Segmento
from .ufs import CODIGOS_UF

CLASSES = 5


def escala_quantil(segmentos: list[Segmento], casas_decimais: int) -> Escala:
    """Limites de 5 classes por quantis dos valores das UFs (o total BR fica de fora)."""
    valores = [
        p.v
        for seg in segmentos
        for geo, serie in seg.valores.items()
        if geo in CODIGOS_UF
        for p in serie.values()
        if p.v is not None
    ]
    if len(valores) < CLASSES:
        raise ValueError("valores insuficientes para calcular a escala")
    limites = statistics.quantiles(valores, n=CLASSES, method="inclusive")
    # Arredonda na mesma precisão exibida, para a legenda mostrar exatamente o limite usado.
    return Escala(tipo="quantil", limites=[round(x, casas_decimais) for x in limites])
