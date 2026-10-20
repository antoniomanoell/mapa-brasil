"""Linha de comando: `uv run indicadores build [--only <id>]`."""

import argparse
import sys
from datetime import date

from .build import executar
from .indicators import DEFINICOES
from .paths import REPORT


def build(only: str | None, hoje: date | None = None) -> int:
    if only is not None and only not in DEFINICOES:
        disponiveis = ", ".join(sorted(DEFINICOES)) or "nenhum"
        print(f"Indicador desconhecido: {only!r}. Disponíveis: {disponiveis}.", file=sys.stderr)
        return 2
    exe = executar(DEFINICOES, only, hoje or date.today())
    for id_, (_, res) in exe.resultados.items():
        status = "ok" if res.ok else f"FALHOU ({len(res.erros)} erros)"
        print(f"{id_}: {status}, {len(res.alertas)} alertas")
    print(f"Relatório: {REPORT}")
    return 0 if exe.ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="indicadores")
    sub = parser.add_subparsers(dest="comando", required=True)
    p_build = sub.add_parser("build", help="reconstrói data/public/")
    p_build.add_argument("--only", metavar="ID", help="reconstrói apenas este indicador")

    args = parser.parse_args(argv)
    if args.comando == "build":
        return build(args.only)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
