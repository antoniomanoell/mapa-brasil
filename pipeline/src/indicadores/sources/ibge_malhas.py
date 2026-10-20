"""Malha das UFs pela API de malhas do IBGE, já em TopoJSON (PROJECT.md, 6.4)."""

import json
from pathlib import Path
from typing import Any

from ..paths import PUBLIC_GEO
from ..ufs import CODIGOS_UF
from .http import baixar_json

URL = "https://servicodados.ibge.gov.br/api/v4/malhas/paises/BR"
# Fronteiras estaduais idênticas de 2022 a 2025 nesta API (conferido em 2026-10-20).
# "intermediaria" ≈ 87 KB (30 KB gzip), dentro do alvo de 150 KB.
PARAMS = {
    "intrarregiao": "UF",
    "formato": "application/json",
    "qualidade": "intermediaria",
    "periodo": "2025",
}
OBJETO = "BRUF"


def conferir(topo: Any) -> None:
    if topo.get("type") != "Topology" or OBJETO not in topo.get("objects", {}):
        raise ValueError(f"malha do IBGE sem objeto {OBJETO!r}: formato da API mudou?")
    codigos = {g["properties"]["codarea"] for g in topo["objects"][OBJETO]["geometries"]}
    if codigos != CODIGOS_UF:
        raise ValueError(f"malha com códigos de UF inesperados: {sorted(codigos ^ CODIGOS_UF)}")


def construir(destino_dir: Path = PUBLIC_GEO) -> Path:
    topo = baixar_json(URL, PARAMS)
    conferir(topo)
    destino_dir.mkdir(parents=True, exist_ok=True)
    destino = destino_dir / "uf.topojson"
    destino.write_text(json.dumps(topo, separators=(",", ":")), encoding="utf-8")
    return destino
