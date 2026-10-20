"""As 27 UFs, chaveadas pelo código IBGE de 2 dígitos.

Conferido com https://servicodados.ibge.gov.br/api/v1/localidades/estados em 2026-10-20.
"""

from typing import NamedTuple


class UF(NamedTuple):
    codigo: str
    sigla: str
    nome: str
    regiao: str


UFS: tuple[UF, ...] = (
    UF("11", "RO", "Rondônia", "N"),
    UF("12", "AC", "Acre", "N"),
    UF("13", "AM", "Amazonas", "N"),
    UF("14", "RR", "Roraima", "N"),
    UF("15", "PA", "Pará", "N"),
    UF("16", "AP", "Amapá", "N"),
    UF("17", "TO", "Tocantins", "N"),
    UF("21", "MA", "Maranhão", "NE"),
    UF("22", "PI", "Piauí", "NE"),
    UF("23", "CE", "Ceará", "NE"),
    UF("24", "RN", "Rio Grande do Norte", "NE"),
    UF("25", "PB", "Paraíba", "NE"),
    UF("26", "PE", "Pernambuco", "NE"),
    UF("27", "AL", "Alagoas", "NE"),
    UF("28", "SE", "Sergipe", "NE"),
    UF("29", "BA", "Bahia", "NE"),
    UF("31", "MG", "Minas Gerais", "SE"),
    UF("32", "ES", "Espírito Santo", "SE"),
    UF("33", "RJ", "Rio de Janeiro", "SE"),
    UF("35", "SP", "São Paulo", "SE"),
    UF("41", "PR", "Paraná", "S"),
    UF("42", "SC", "Santa Catarina", "S"),
    UF("43", "RS", "Rio Grande do Sul", "S"),
    UF("50", "MS", "Mato Grosso do Sul", "CO"),
    UF("51", "MT", "Mato Grosso", "CO"),
    UF("52", "GO", "Goiás", "CO"),
    UF("53", "DF", "Distrito Federal", "CO"),
)

CODIGOS_UF: frozenset[str] = frozenset(uf.codigo for uf in UFS)
BR = "BR"
# Toda série publicada cobre as 27 UFs mais o total nacional.
GEOS_OBRIGATORIAS: frozenset[str] = CODIGOS_UF | {BR}
