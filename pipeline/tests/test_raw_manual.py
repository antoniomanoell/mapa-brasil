import re

import pytest

from indicadores.raw_manual import ErroEntradaManual, exigir, sha256


def _manifest(raiz, sha):
    (raiz / "MANIFEST.yaml").write_text(
        "arquivos:\n"
        "  - arquivo: fonte/dados.csv\n"
        "    url: https://exemplo.gov.br/dados.csv\n"
        "    baixado_em: 2026-10-20\n"
        f"    sha256: {sha}\n",
        encoding="utf-8",
    )


def test_arquivo_ausente_diz_de_onde_baixar(tmp_path):
    _manifest(tmp_path, "0" * 64)
    with pytest.raises(ErroEntradaManual, match=re.escape("https://exemplo.gov.br/dados.csv")):
        exigir("fonte/dados.csv", tmp_path)


def test_fora_do_manifest(tmp_path):
    _manifest(tmp_path, "0" * 64)
    with pytest.raises(ErroEntradaManual, match="não está no MANIFEST"):
        exigir("outro.csv", tmp_path)


def test_hash_divergente_e_correto(tmp_path):
    arq = tmp_path / "fonte" / "dados.csv"
    arq.parent.mkdir()
    arq.write_bytes(b"a,b\n1,2\n")
    _manifest(tmp_path, "0" * 64)
    with pytest.raises(ErroEntradaManual, match="não confere"):
        exigir("fonte/dados.csv", tmp_path)
    _manifest(tmp_path, sha256(arq))
    assert exigir("fonte/dados.csv", tmp_path) == arq
