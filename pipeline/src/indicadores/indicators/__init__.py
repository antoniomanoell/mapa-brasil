"""Um módulo por indicador: busca → transforma → valida → emite."""

from .analfabetismo import Analfabetismo
from .base import DefinicaoIndicador
from .esgoto import Esgoto
from .gini import Gini
from .homicidios import Homicidios
from .idhm import Idhm
from .pnadc_anual import desocupacao, informalidade
from .projecoes import esperanca_vida, mort_infantil
from .renda_pc import RendaPc

# Registro dos indicadores implementados, na ordem do seletor.
DEFINICOES: dict[str, DefinicaoIndicador] = {
    d.id: d
    for d in (
        Idhm(),
        RendaPc(),
        Gini(),
        desocupacao(),
        informalidade(),
        Analfabetismo(),
        esperanca_vida(),
        mort_infantil(),
        Esgoto(),
        Homicidios(),
    )
}
