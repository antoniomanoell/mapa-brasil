"""Arquivos baixados à mão, conferidos contra raw_manual/MANIFEST.yaml (PROJECT.md, 6.2)."""

import hashlib
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

from .paths import RAW_MANUAL


class ErroEntradaManual(Exception):
    pass


@dataclass(frozen=True)
class EntradaManual:
    arquivo: str
    url: str
    baixado_em: date
    sha256: str
    descricao: str = ""


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


def exigir(arquivo: str, raiz: Path = RAW_MANUAL) -> Path:
    """Devolve o caminho do arquivo manual, ou falha dizendo o que baixar e de onde."""
    entrada = carregar_manifest(raiz).get(arquivo)
    if entrada is None:
        raise ErroEntradaManual(
            f"{arquivo} não está no MANIFEST.yaml. Registre URL, data de download e sha256."
        )
    caminho = raiz / arquivo
    if not caminho.exists():
        raise ErroEntradaManual(
            f"Falta o arquivo manual {caminho}.\n"
            f"  Baixe de: {entrada.url}\n"
            f"  e salve como: pipeline/raw_manual/{arquivo}"
            + (f"\n  ({entrada.descricao})" if entrada.descricao else "")
        )
    obtido = sha256(caminho)
    if obtido != entrada.sha256:
        raise ErroEntradaManual(
            f"sha256 de {arquivo} não confere com o MANIFEST.yaml.\n"
            f"  esperado: {entrada.sha256}\n  obtido:   {obtido}\n"
            f"  Se a fonte publicou nova versão, baixe de novo de {entrada.url}, "
            f"atualize o MANIFEST e revise o diff dos dados."
        )
    return caminho
