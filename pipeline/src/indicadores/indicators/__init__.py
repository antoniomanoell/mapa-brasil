"""Um módulo por indicador: busca → transforma → valida → emite."""

from .base import DefinicaoIndicador
from .homicidios import Homicidios
from .idhm import Idhm
from .renda_pc import RendaPc

# Registro dos indicadores implementados, na ordem do seletor.
DEFINICOES: dict[str, DefinicaoIndicador] = {d.id: d for d in (Idhm(), RendaPc(), Homicidios())}
