"""GET com cache em disco (pipeline/cache/, fora do git), para o build ser repetível."""

import hashlib
import json
from pathlib import Path
from typing import Any

import httpx

from ..paths import CACHE

TIMEOUT = httpx.Timeout(120.0, connect=30.0)


def _chave(url: str, params: dict[str, str] | None) -> str:
    bruto = json.dumps([url, sorted((params or {}).items())])
    return hashlib.sha256(bruto.encode()).hexdigest()[:24]


def baixar(
    url: str,
    params: dict[str, str] | None = None,
    *,
    usar_cache: bool = True,
    cache_dir: Path = CACHE,
) -> bytes:
    destino = cache_dir / _chave(url, params)
    if usar_cache and destino.exists():
        return destino.read_bytes()
    resp = httpx.get(url, params=params, timeout=TIMEOUT, follow_redirects=True)
    resp.raise_for_status()
    cache_dir.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(resp.content)
    return resp.content


def baixar_json(url: str, params: dict[str, str] | None = None, *, usar_cache: bool = True) -> Any:
    return json.loads(baixar(url, params, usar_cache=usar_cache))
