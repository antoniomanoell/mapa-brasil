"""HTTP com cache em disco (pipeline/cache/, fora do git), para o build ser repetível.

A data de extração de um dado é a data em que a resposta entrou no cache. Apagar o cache força
uma nova extração.
"""

import hashlib
import json
import ssl
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import httpx
import truststore

from ..paths import CACHE

TIMEOUT = httpx.Timeout(120.0, connect=30.0)
# Valida certificados pelo repositório do sistema operacional (como o navegador e o curl), que
# completa cadeias sem o certificado intermediário — caso de download.inep.gov.br. A verificação
# nunca é desligada.
VERIFICACAO = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
TENTATIVAS = 4
INTERVALO_MINIMO = 1.0  # segundos entre requisições
CABECALHOS = {"User-Agent": "IndicadoresBR/0.1 (+https://github.com/antoniomanoell/mapa-brasil)"}
_ultima_requisicao = 0.0


@dataclass(frozen=True)
class Resposta:
    conteudo: bytes
    obtido_em: date


def _chave(url: str, params: dict[str, str] | None, corpo: bytes | None) -> str:
    bruto = json.dumps([url, sorted((params or {}).items())]).encode() + (corpo or b"")
    return hashlib.sha256(bruto).hexdigest()[:24]


def requisitar(
    url: str,
    params: dict[str, str] | None = None,
    *,
    corpo: bytes | None = None,
    usar_cache: bool = True,
    cache_dir: Path = CACHE,
) -> Resposta:
    """GET (ou POST, se houver `corpo`) com cache."""
    destino = cache_dir / _chave(url, params, corpo)
    if not (usar_cache and destino.exists()):
        resp = _com_tentativas(url, params, corpo)
        cache_dir.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(resp.content)
    return Resposta(destino.read_bytes(), date.fromtimestamp(destino.stat().st_mtime))


def _com_tentativas(url: str, params: dict[str, str] | None, corpo: bytes | None) -> httpx.Response:
    """Servidores públicos (TabNet, SIDRA) às vezes derrubam conexões: tenta de novo com espera.

    Também espaça as requisições, para não sobrecarregar servidores públicos.
    """
    global _ultima_requisicao
    for tentativa in range(TENTATIVAS):
        time.sleep(max(0.0, _ultima_requisicao + INTERVALO_MINIMO - time.monotonic()))
        _ultima_requisicao = time.monotonic()
        try:
            if corpo is None:
                resp = httpx.get(
                    url,
                    params=params,
                    headers=CABECALHOS,
                    timeout=TIMEOUT,
                    verify=VERIFICACAO,
                    follow_redirects=True,
                )
            else:
                resp = httpx.post(
                    url,
                    params=params,
                    content=corpo,
                    headers={**CABECALHOS, "Content-Type": "application/x-www-form-urlencoded"},
                    timeout=TIMEOUT,
                    verify=VERIFICACAO,
                )
            if resp.status_code < 500:
                resp.raise_for_status()
                return resp
        except httpx.TransportError:
            if tentativa == TENTATIVAS - 1:
                raise
        time.sleep(5 * 3**tentativa)
    resp.raise_for_status()
    return resp


def baixar(url: str, params: dict[str, str] | None = None, *, usar_cache: bool = True) -> bytes:
    return requisitar(url, params, usar_cache=usar_cache).conteudo


def baixar_json(url: str, params: dict[str, str] | None = None, *, usar_cache: bool = True) -> Any:
    return json.loads(baixar(url, params, usar_cache=usar_cache))
