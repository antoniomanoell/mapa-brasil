"""INEP — resultados do Ideb 2025 (série 2005–2025), planilhas de Brasil e de UFs.

Cada etapa é uma aba; cada linha é uma geografia + rede. As colunas do Ideb observado são achadas
pelo código no cabeçalho (`VL_OBSERVADO_AAAA`), e a rede pelo rótulo sem as notas entre parênteses
("Pública (4)" → "Pública").
"""

import io
import re
import zipfile
from functools import cache

import openpyxl

from ..raw_manual import exigir
from ..ufs import BR, UFS

ARQUIVO_UFS = "inep_ideb/divulgacao_regioes_ufs_ideb_2025.zip"
ARQUIVO_BRASIL = "inep_ideb/divulgacao_brasil_ideb_2025.zip"
URL = (
    "https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/"
    "ideb/resultados"
)
# A planilha do INEP abrevia três nomes.
_ABREVIADOS = {"R. G. do Norte": "24", "R. G. do Sul": "43", "M. G. do Sul": "50"}
_NOMES = {"Brasil": BR, **{uf.nome: uf.codigo for uf in UFS}, **_ABREVIADOS}
_OBSERVADO = re.compile(r"VL_OBSERVADO_(\d{4})")
_CABECALHO = re.compile(r"IDEB (\d{4})\d? \(N x P\)")

# etapa → (aba nas UFs, aba no Brasil)
ABAS = {
    "anos_iniciais": ("UF e Regiões (AI)", "Brasil (Anos Iniciais)"),
    "anos_finais": ("UF e Regiões (AF)", "Brasil (Anos Finais)"),
    "medio": ("UF e Regiões (EM)", "Brasil (EM)"),
}

Serie = dict[str, dict[int, float | None]]  # geo → ano → Ideb (None = não calculado pelo INEP)


def _rede(rotulo: object) -> str:
    return re.sub(r"\s*\(.*$", "", str(rotulo)).strip()


def ler_aba(linhas: list[tuple], rede: str) -> Serie:
    linha_cod = next(
        i for i, r in enumerate(linhas) if any(_OBSERVADO.fullmatch(str(c)) for c in r)
    )
    colunas = {
        i: int(m.group(1))
        for i, c in enumerate(linhas[linha_cod])
        if (m := _OBSERVADO.fullmatch(str(c).strip()))
    }
    # Algumas colunas vêm sem código (ex.: Ideb 2023 dos anos finais na planilha do Brasil); aí
    # vale o cabeçalho de texto "IDEB AAAA (N x P)" das linhas acima.
    for linha in linhas[max(0, linha_cod - 4) : linha_cod]:
        for i, c in enumerate(linha):
            m = _CABECALHO.fullmatch(" ".join(str(c).split()))
            if m and i not in colunas and int(m.group(1)) not in colunas.values():
                colunas[i] = int(m.group(1))
    saida: Serie = {}
    for r in linhas[linha_cod + 1 :]:
        if not r or r[0] is None:
            continue
        geo = _NOMES.get(str(r[0]).strip())
        if geo is None or _rede(r[1]) != rede or geo in saida:
            continue
        saida[geo] = {
            ano: (float(r[i]) if isinstance(r[i], (int, float)) else None)
            for i, ano in colunas.items()
        }
    return saida


def _linhas(arquivo: str, aba: str) -> list[tuple]:
    zf = zipfile.ZipFile(exigir(arquivo))
    nome = next(n for n in zf.namelist() if n.endswith(".xlsx"))
    wb = openpyxl.load_workbook(io.BytesIO(zf.read(nome)), read_only=True, data_only=True)
    return list(wb[aba].iter_rows(values_only=True))


@cache
def etapa(etapa_id: str, rede: str) -> Serie:
    aba_ufs, aba_br = ABAS[etapa_id]
    saida = ler_aba(_linhas(ARQUIVO_UFS, aba_ufs), rede)
    saida |= ler_aba(_linhas(ARQUIVO_BRASIL, aba_br), rede)
    faltando = ({BR} | {uf.codigo for uf in UFS}) - set(saida)
    if faltando:
        raise ValueError(f"Ideb {etapa_id}, rede {rede}: geografias ausentes {sorted(faltando)}")
    return saida
