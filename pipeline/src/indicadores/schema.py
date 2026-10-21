"""Modelos do formato publicado em data/public/ (PROJECT.md, seção 7)."""

from datetime import date
from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

# "BR", UF (2 dígitos) ou município (7 dígitos, fase futura).
CodigoGeo = Annotated[str, StringConstraints(pattern=r"^(BR|\d{2}|\d{7})$")]
Ano = Annotated[str, StringConstraints(pattern=r"^\d{4}$")]
Id = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_]*$")]


class Modelo(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Flag(StrEnum):
    BAIXA_PRECISAO = "baixa_precisao"
    COBERTURA_URBANA = "cobertura_urbana"
    ESTIMATIVA = "estimativa"
    # Nunca publicado: existe para o validador recusar dado preliminar.
    PRELIMINAR = "preliminar"


class Ponto(Modelo):
    """Valor de uma geografia num ano. `v=None` exige `lacuna` com o motivo."""

    v: float | None
    # Numerador em contagem absoluta, quando o projeto calcula a taxa (ex.: nº de homicídios).
    n: float | None = None
    cv: float | None = None
    ic: tuple[float, float] | None = None
    flags: list[Flag] = Field(default_factory=list)
    lacuna: str | None = None

    @model_validator(mode="after")
    def _lacuna_explicita(self) -> Self:
        if (self.v is None) != (self.lacuna is not None):
            raise ValueError("v=None exige `lacuna` preenchida, e vice-versa")
        return self


class Segmento(Modelo):
    """Trecho da série com metodologia homogênea. Segmentos nunca são emendados."""

    id: Id
    subindicador: Id
    # "referencia": série de apoio mostrada só no painel da UF (ex.: taxa direta do DATASUS para a
    # mortalidade infantil); não entra no mapa, no ranking, na escala nem no slider.
    papel: Literal["principal", "referencia"] = "principal"
    rotulo: str
    fonte: str
    fonte_url: str
    tabela: str
    extraido_em: date
    notas: str = ""
    # Anos que o segmento publica. Anos do intervalo fora desta lista são lacunas do
    # segmento inteiro (ex.: 2010 na PNAD) e devem ser explicados em `notas`.
    anos: list[int]
    valores: dict[CodigoGeo, dict[Ano, Ponto]]

    @model_validator(mode="after")
    def _anos_coerentes(self) -> Self:
        if self.anos != sorted(set(self.anos)):
            raise ValueError(f"{self.id}: `anos` deve ser crescente e sem repetição")
        declarados = {str(a) for a in self.anos}
        for geo, serie in self.valores.items():
            extras = set(serie) - declarados
            if extras:
                raise ValueError(f"{self.id}/{geo}: anos fora de `anos`: {sorted(extras)}")
        return self


class Subindicador(Modelo):
    id: Id
    nome: str


class Quebra(Modelo):
    ano: int
    texto: str


class Escala(Modelo):
    tipo: Literal["quantil"]
    # n-1 limites para n classes, calculados sobre todos os anos e segmentos.
    limites: list[float]


class Indicador(Modelo):
    id: Id
    nome: str
    tema: str
    unidade: str
    unidade_detalhe: str
    direcao: Literal["maior_melhor", "menor_melhor"]
    casas_decimais: int = Field(ge=0, le=4)
    tipo_valor: Literal["medido", "estimativa"]
    # Sempre ao menos um; indicadores simples têm um único subindicador.
    subindicadores: list[Subindicador] = Field(min_length=1)
    segmentos: list[Segmento] = Field(min_length=1)
    quebras: list[Quebra] = Field(default_factory=list)
    escalas: dict[Id, Escala]
    versao_pipeline: str

    @model_validator(mode="after")
    def _referencias_internas(self) -> Self:
        subs = {s.id for s in self.subindicadores}
        for seg in self.segmentos:
            if seg.subindicador not in subs:
                raise ValueError(
                    f"segmento {seg.id}: subindicador {seg.subindicador!r} inexistente"
                )
        chaves = [(s.subindicador, s.id) for s in self.segmentos]
        if len(chaves) != len(set(chaves)):
            raise ValueError("segmentos repetidos para o mesmo subindicador")
        if set(self.escalas) != subs:
            raise ValueError("`escalas` deve ter exatamente uma entrada por subindicador")
        return self


class ItemCatalogo(Modelo):
    id: Id
    nome: str
    tema: str
    unidade: str
    subindicadores: list[Subindicador]
    ano_inicial: int
    ano_final: int
    arquivo: str


class Catalogo(Modelo):
    gerado_em: date
    versao_pipeline: str
    indicadores: list[ItemCatalogo]
