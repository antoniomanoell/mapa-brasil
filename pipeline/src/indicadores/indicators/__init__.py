"""Um módulo por indicador: busca → transforma → valida → emite."""

from .base import DefinicaoIndicador

# Registro dos indicadores implementados, na ordem do seletor.
DEFINICOES: dict[str, DefinicaoIndicador] = {}
