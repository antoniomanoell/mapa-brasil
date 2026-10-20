"""Checagens da seção 8 do PROJECT.md.

Erros fazem o build falhar; alertas vão para o REPORT.md para revisão humana.
"""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Literal

import yaml

from .schema import Flag, Indicador
from .ufs import BR, GEOS_OBRIGATORIAS

# Tolerância padrão da conferência com números publicados (arredondamento).
TOLERANCIA_PADRAO = 0.01
LIMIAR_CV_PADRAO = 15.0


@dataclass(frozen=True)
class Regras:
    """Regras de validação declaradas por cada indicador."""

    faixa: tuple[float, float]
    # Variação relativa ano a ano acima disto gera alerta (0,25 = 25%).
    limiar_variacao: float
    # Intervalo de anos válido para cada metodologia (id do segmento → (início, fim)).
    metodologias: dict[str, tuple[int, int | None]]
    limiar_cv: float = LIMIAR_CV_PADRAO


@dataclass(frozen=True)
class Referencia:
    """Valor divulgado oficialmente, usado para conferir a saída do pipeline."""

    indicador: str
    subindicador: str
    segmento: str
    geo: str
    ano: int
    valor: float
    url: str
    tolerancia: float = TOLERANCIA_PADRAO
    # "valor" compara com `Ponto.v`; "contagem", com o numerador `Ponto.n`.
    medida: Literal["valor", "contagem"] = "valor"


@dataclass
class Resultado:
    erros: list[str] = field(default_factory=list)
    alertas: list[str] = field(default_factory=list)
    conferencias: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.erros


def ultimo_ano_transcorrido(hoje: date) -> int:
    return hoje.year - 1


def carregar_referencias(caminho: Path) -> list[Referencia]:
    if not caminho.exists():
        return []
    dados = yaml.safe_load(caminho.read_text(encoding="utf-8")) or {}
    return [Referencia(**r) for r in dados.get("referencias") or []]


def validar(ind: Indicador, regras: Regras, referencias: list[Referencia], hoje: date) -> Resultado:
    r = Resultado()
    _cobertura(ind, r)
    _pontos(ind, regras, r)
    _sem_projecoes(ind, hoje, r)
    _sem_emenda(ind, regras, r)
    _escalas(ind, r)
    _variacao(ind, regras, r)
    _conferencia(ind, [ref for ref in referencias if ref.indicador == ind.id], r)
    return r


def _cobertura(ind: Indicador, r: Resultado) -> None:
    for seg in ind.segmentos:
        for geo in sorted(GEOS_OBRIGATORIAS):
            serie = seg.valores.get(geo, {})
            faltando = [a for a in seg.anos if str(a) not in serie]
            if faltando:
                r.erros.append(
                    f"{seg.subindicador}/{seg.id}: {geo} sem valor nem lacuna explícita em "
                    f"{faltando}"
                )


def _pontos(ind: Indicador, regras: Regras, r: Resultado) -> None:
    lo, hi = regras.faixa
    for seg in ind.segmentos:
        for geo, serie in seg.valores.items():
            for ano, p in serie.items():
                onde = f"{seg.subindicador}/{seg.id}/{geo}/{ano}"
                if Flag.PRELIMINAR in p.flags:
                    r.erros.append(f"{onde}: dado preliminar não pode ser publicado")
                if p.v is not None and not lo <= p.v <= hi:
                    r.erros.append(f"{onde}: {p.v} fora da faixa plausível [{lo}, {hi}]")
                if (
                    p.cv is not None
                    and p.cv > regras.limiar_cv
                    and Flag.BAIXA_PRECISAO not in p.flags
                ):
                    r.erros.append(
                        f"{onde}: CV {p.cv} > {regras.limiar_cv} sem flag baixa_precisao"
                    )
                if (
                    ind.tipo_valor == "estimativa"
                    and p.v is not None
                    and Flag.ESTIMATIVA not in p.flags
                ):
                    r.erros.append(f"{onde}: indicador estimado sem flag estimativa")


def _sem_projecoes(ind: Indicador, hoje: date, r: Resultado) -> None:
    limite = ultimo_ano_transcorrido(hoje)
    for seg in ind.segmentos:
        futuros = [a for a in seg.anos if a > limite]
        if futuros:
            r.erros.append(
                f"{seg.subindicador}/{seg.id}: anos posteriores a {limite} (projeção): {futuros}"
            )


def _sem_emenda(ind: Indicador, regras: Regras, r: Resultado) -> None:
    for seg in ind.segmentos:
        if seg.id not in regras.metodologias:
            r.erros.append(f"{seg.id}: metodologia não declarada nas regras do indicador")
            continue
        inicio, fim = regras.metodologias[seg.id]
        fora = [a for a in seg.anos if a < inicio or (fim is not None and a > fim)]
        if fora:
            r.erros.append(
                f"{seg.subindicador}/{seg.id}: anos {fora} fora do intervalo da metodologia "
                f"({inicio}–{fim or '…'})"
            )


def _escalas(ind: Indicador, r: Resultado) -> None:
    for sub, esc in ind.escalas.items():
        if esc.limites != sorted(esc.limites):
            r.erros.append(f"escala de {sub}: limites fora de ordem")


def _variacao(ind: Indicador, regras: Regras, r: Resultado) -> None:
    for seg in ind.segmentos:
        for geo, serie in sorted(seg.valores.items()):
            anterior: tuple[int, float] | None = None
            for ano in seg.anos:
                p = serie.get(str(ano))
                if p is None or p.v is None:
                    anterior = None
                    continue
                # Só compara pontos próximos (anual ou bienal, como o IDEB). Censos decenais ficam
                # de fora: uma década de mudança não é "variação ano a ano".
                if anterior is not None and anterior[1] != 0 and ano - anterior[0] <= 2:
                    var = (p.v - anterior[1]) / abs(anterior[1])
                    if abs(var) > regras.limiar_variacao:
                        r.alertas.append(
                            f"{seg.subindicador}/{seg.id}/{geo}: {anterior[0]}→{ano} variou "
                            f"{var:+.1%} ({anterior[1]} → {p.v})"
                        )
                anterior = (ano, p.v)


def _conferencia(ind: Indicador, refs: list[Referencia], r: Resultado) -> None:
    if len(refs) < 3:
        r.erros.append(f"conferência: {len(refs)} valores de referência (mínimo 3)")
    ultimo_br = _ultimo_ano_br(ind)
    if ultimo_br is not None and not any(
        ref.geo == BR and (ref.subindicador, ref.segmento, ref.ano) == ultimo_br for ref in refs
    ):
        r.erros.append(
            f"conferência: falta referência do Brasil no ano mais recente "
            f"({ultimo_br[0]}/{ultimo_br[1]}/{ultimo_br[2]})"
        )

    segs = {(s.subindicador, s.id): s for s in ind.segmentos}
    for ref in refs:
        onde = f"{ref.subindicador}/{ref.segmento}/{ref.geo}/{ref.ano} ({ref.medida})"
        seg = segs.get((ref.subindicador, ref.segmento))
        p = seg.valores.get(ref.geo, {}).get(str(ref.ano)) if seg else None
        calculado = (p.n if ref.medida == "contagem" else p.v) if p else None
        if calculado is None:
            r.erros.append(f"conferência {onde}: sem valor calculado para comparar")
            continue
        dif = abs(calculado - ref.valor)
        if dif > ref.tolerancia:
            r.erros.append(
                f"conferência {onde}: calculado {calculado} ≠ publicado {ref.valor} "
                f"(dif. {dif:.4g} > {ref.tolerancia})"
            )
        else:
            r.conferencias.append(f"{onde}: {calculado} ≈ {ref.valor} ✓ ({ref.url})")


def _ultimo_ano_br(ind: Indicador) -> tuple[str, str, int] | None:
    """(subindicador, segmento, ano) do valor mais recente do Brasil no 1º subindicador."""
    principal = ind.subindicadores[0].id
    melhor: tuple[str, str, int] | None = None
    for seg in ind.segmentos:
        if seg.subindicador != principal:
            continue
        for ano in seg.anos:
            p = seg.valores.get(BR, {}).get(str(ano))
            if p is not None and p.v is not None and (melhor is None or ano > melhor[2]):
                melhor = (seg.subindicador, seg.id, ano)
    return melhor
