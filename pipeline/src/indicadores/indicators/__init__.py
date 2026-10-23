"""Um módulo por indicador: busca → transforma → valida → emite."""

from .analfabetismo import Analfabetismo
from .base import DefinicaoIndicador
from .esgoto import Esgoto
from .gini import Gini
from .homicidios import Homicidios
from .ideb import Ideb
from .idhm import Idhm
from .inflacao import Inflacao
from .pib_pc import PibPc
from .pnadc_anual import desocupacao, informalidade
from .pobreza import extrema_pobreza, pobreza
from .projecoes import esperanca_vida, mort_infantil
from .renda_pc import RendaPc

# Registro dos indicadores implementados, na ordem do seletor.
DEFINICOES: dict[str, DefinicaoIndicador] = {
    d.id: d
    for d in (
        Idhm(),
        RendaPc(),
        PibPc(),
        Gini(),
        pobreza(),
        extrema_pobreza(),
        desocupacao(),
        informalidade(),
        Analfabetismo(),
        Ideb(),
        esperanca_vida(),
        mort_infantil(),
        Esgoto(),
        Homicidios(),
        Inflacao(),
    )
}
