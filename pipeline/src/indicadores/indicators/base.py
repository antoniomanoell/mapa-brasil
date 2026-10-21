from datetime import date
from typing import Protocol

from ..schema import Indicador
from ..validate import Regras


class DefinicaoIndicador(Protocol):
    """Contrato de cada módulo em indicators/: busca → transforma → emite.

    Opcionalmente, `construir` preenche um atributo `auxiliares` (validate.Auxiliares) com séries
    de conferência indireta, que o validador compara com referências `medida: auxiliar`.
    """

    id: str
    regras: Regras

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador: ...
