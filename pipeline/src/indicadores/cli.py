"""Linha de comando: `uv run indicadores build [--only <id>]`."""

import argparse
import sys

# Preenchido na Fase 1, à medida que cada indicador ganha seu módulo.
INDICADORES: dict[str, object] = {}


def build(only: str | None) -> int:
    if only is not None and only not in INDICADORES:
        disponiveis = ", ".join(sorted(INDICADORES)) or "nenhum"
        print(f"Indicador desconhecido: {only!r}. Disponíveis: {disponiveis}.", file=sys.stderr)
        return 2
    if not INDICADORES:
        print("Nenhum indicador implementado ainda.")
        return 0
    return 0


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
