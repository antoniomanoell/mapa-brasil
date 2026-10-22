"""Arquivos de fonte sem API, conferidos contra raw_manual/MANIFEST.yaml (PROJECT.md, 6.2).

Entradas com `automatico: true` têm URL estável de download direto. O pipeline as baixa sozinho
quando faltam. As demais o mantenedor baixa à mão. Em ambos os casos o sha256 precisa bater com o
MANIFEST: se a fonte publicar nova versão, o build falha até alguém revisar e atualizar o hash.
"""

import hashlib
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import httpx
import yaml

from .paths import RAW_MANUAL
from .sources.http import CABECALHOS, TENTATIVAS, TIMEOUT, VERIFICACAO


class ErroEntradaManual(Exception):
    pass


@dataclass(frozen=True)
class EntradaManual:
    arquivo: str
    url: str
    baixado_em: date
    sha256: str
    descricao: str = ""
    automatico: bool = False


def sha256(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def carregar_manifest(raiz: Path = RAW_MANUAL) -> dict[str, EntradaManual]:
    dados = yaml.safe_load((raiz / "MANIFEST.yaml").read_text(encoding="utf-8")) or {}
    entradas = [EntradaManual(**e) for e in dados.get("arquivos") or []]
    return {e.arquivo: e for e in entradas}


def _baixar(url: str, destino: Path) -> None:
    """Baixa com novas tentativas: servidores públicos às vezes derrubam a conexão."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporario = destino.with_suffix(destino.suffix + ".parcial")
    for tentativa in range(TENTATIVAS):
        try:
            with httpx.stream(
                "GET",
                url,
                headers=CABECALHOS,
                timeout=TIMEOUT,
                verify=VERIFICACAO,
                follow_redirects=True,
            ) as resp:
                resp.raise_for_status()
                with temporario.open("wb") as f:
                    for bloco in resp.iter_bytes():
                        f.write(bloco)
            break
        except httpx.TransportError:
            if tentativa == TENTATIVAS - 1:
                raise
            time.sleep(5 * 3**tentativa)
    temporario.replace(destino)


def exigir(arquivo: str, raiz: Path = RAW_MANUAL) -> Path:
    """Devolve o caminho do arquivo conferido, ou falha dizendo o que baixar e de onde."""
    entrada = carregar_manifest(raiz).get(arquivo)
    if entrada is None:
        raise ErroEntradaManual(
            f"{arquivo} não está no MANIFEST.yaml. Registre URL, data de download e sha256."
        )
    caminho = raiz / arquivo
    if not caminho.exists():
        if not entrada.automatico:
            raise ErroEntradaManual(
                f"Falta o arquivo manual {caminho}.\n"
                f"  Baixe de: {entrada.url}\n"
                f"  e salve como: pipeline/raw_manual/{arquivo}"
                + (f"\n  ({entrada.descricao})" if entrada.descricao else "")
            )
        _baixar(entrada.url, caminho)
    obtido = sha256(caminho)
    if obtido != entrada.sha256:
        raise ErroEntradaManual(
            f"sha256 de {arquivo} não confere com o MANIFEST.yaml.\n"
            f"  esperado: {entrada.sha256}\n  obtido:   {obtido}\n"
            f"  Se a fonte publicou nova versão, baixe de novo de {entrada.url}, "
            f"atualize o MANIFEST e revise o diff dos dados."
        )
    return caminho
