"""Gera pipeline/REPORT.md (PROJECT.md, 6.3)."""

from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING

from .paths import escrever
from .schema import Indicador, Segmento
from .validate import Resultado

if TYPE_CHECKING:
    from .build import Execucao


def _faixas(anos: list[int]) -> str:
    """[2001, 2002, 2003, 2005] → '2001–2003, 2005'."""
    if not anos:
        return "—"
    partes: list[str] = []
    inicio = fim = anos[0]
    for a in anos[1:]:
        if a == fim + 1:
            fim = a
            continue
        partes.append(f"{inicio}–{fim}" if fim > inicio else str(inicio))
        inicio = fim = a
    partes.append(f"{inicio}–{fim}" if fim > inicio else str(inicio))
    return ", ".join(partes)


def _lacunas_segmento(seg: Segmento) -> list[int]:
    return (
        [a for a in range(seg.anos[0], seg.anos[-1] + 1) if a not in seg.anos] if seg.anos else []
    )


def _secao(id_: str, ind: Indicador | None, res: Resultado) -> list[str]:
    linhas = [f"## `{id_}` — {'OK' if res.ok else 'FALHOU'}", ""]
    if ind is not None:
        linhas += [
            "| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |",
            "|---|---|---|---|---|",
        ]
        for seg in ind.segmentos:
            flags = Counter(
                f.value for serie in seg.valores.values() for p in serie.values() for f in p.flags
            )
            flags_txt = ", ".join(f"{k}: {n}" for k, n in sorted(flags.items())) or "—"
            linhas.append(
                f"| {seg.subindicador} | {seg.rotulo} | {_faixas(seg.anos)} | "
                f"{_faixas(_lacunas_segmento(seg))} | {flags_txt} |"
            )
        linhas.append("")
        pontuais = [
            f"- {seg.subindicador}/{seg.id}/{geo}/{ano}: {p.lacuna}"
            for seg in ind.segmentos
            for geo, serie in sorted(seg.valores.items())
            for ano, p in sorted(serie.items())
            if p.lacuna
        ]
        if pontuais:
            linhas += ["**Lacunas pontuais**", "", *pontuais, ""]

    for titulo, itens in (
        ("Erros", res.erros),
        ("Alertas (variação suspeita — revisar)", res.alertas),
        ("Conferência com números publicados", res.conferencias),
    ):
        linhas += [f"**{titulo}** ({len(itens)})", ""]
        linhas += [f"- {i}" for i in itens] or ["- nenhum"]
        linhas.append("")
    return linhas


def escrever_report(exe: "Execucao", destino: Path) -> None:
    linhas = [
        "# REPORT do pipeline",
        "",
        f"- Data: {exe.hoje.isoformat()}",
        f"- Versão do pipeline: `{exe.versao}`",
        f"- Escopo: {exe.escopo}",
        f"- Resultado: {'OK' if exe.ok else 'FALHOU'}",
        "",
    ]
    if not exe.resultados:
        linhas += ["Nenhum indicador implementado ainda.", ""]
    for id_, (ind, res) in exe.resultados.items():
        linhas += _secao(id_, ind, res)
    escrever(destino, "\n".join(linhas))
