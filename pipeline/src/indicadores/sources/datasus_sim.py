"""DATASUS — SIM, óbitos por UF de residência, via TabNet (ver FONTES.md)."""

import html
import re
from datetime import date
from urllib.parse import urlencode

from ..ufs import BR, CODIGOS_UF
from .http import requisitar

DEF = "sim/cnv/obt10uf.def"
URL_FORMULARIO = f"http://tabnet.datasus.gov.br/cgi/deftohtm.exe?{DEF}"
URL_CONSULTA = f"http://tabnet.datasus.gov.br/cgi/tabcgi.exe?{DEF}"

# Grupos CID-10 do formulário obt10uf.def (conferidos em 2026-10-20).
GRUPO_AGRESSOES = "246"  # X85–Y09
GRUPO_INTERVENCOES_LEGAIS = "248"  # Y35–Y36 (intervenções legais e operações de guerra)

# Filtros que ficam em "todas as categorias".
_SEM_FILTRO = [
    "SRegião", "SUnidade_da_Federação", "SCapítulo_CID-10", "SCategoria_CID-10",
    "SCausa_-_CID-BR-10", "SCausa_mal_definidas", "SFaixa_Etária", "SFaixa_Etária_OPS",
    "SFaixa_Etária_det", "SFx.Etária_Menor_1A", "SSexo", "SCor/raça", "SEscolaridade",
    "SEstado_civil", "SLocal_ocorrência",
]  # fmt: skip


def anos_preliminares() -> list[int]:
    """Anos que o próprio formulário do TabNet declara como preliminares."""
    pagina = requisitar(URL_FORMULARIO, usar_cache=False).conteudo.decode("latin-1")
    anos = [int(a) for a in re.findall(r"Dados de (\d{4})\s*-\s*Preliminares", pagina)]
    if not anos:
        raise ValueError("TabNet não informa anos preliminares — formato do formulário mudou?")
    return anos


def obitos_por_uf(ano: int, grupos_cid: list[str]) -> tuple[dict[str, int], date]:
    """Óbitos por residência em `ano`, somando os grupos CID-10. Inclui "BR" (Total do TabNet)."""
    campos = [
        ("Linha", "Unidade_da_Federação"),
        ("Coluna", "--Não-Ativa--"),
        ("Incremento", "Óbitos_p/Residênc"),
        ("Arquivos", f"obtuf{ano % 100:02d}.dbf"),
        *[(s, "TODAS_AS_CATEGORIAS__") for s in _SEM_FILTRO],
        *[("SGrupo_CID-10", g) for g in grupos_cid],
        ("zeradas", "exibirlz"),
        ("formato", "prn"),
        ("mostre", "Mostra"),
    ]
    resp = requisitar(URL_CONSULTA, corpo=urlencode(campos, encoding="latin-1").encode())
    return _ler_prn(resp.conteudo.decode("latin-1"), ano), resp.obtido_em


def _ler_prn(pagina: str, ano: int) -> dict[str, int]:
    bloco = re.search(r"<PRE>(.*?)</PRE>", pagina, re.S | re.I)
    if not bloco:
        raise ValueError(f"TabNet {ano}: resposta sem tabela")
    saida: dict[str, int] = {}
    for linha in html.unescape(bloco.group(1)).splitlines():
        partes = [p.strip().strip('"') for p in linha.split(";")]
        # Pula cabeçalho e rodapé: só interessam linhas "rótulo";número.
        if len(partes) != 2 or not re.fullmatch(r"[\d.]+|-", partes[1]):
            continue
        rotulo, valor = partes
        n = 0 if valor in ("-", "") else int(valor.replace(".", ""))
        if rotulo == "Total":
            saida[BR] = n
        elif (cod := rotulo[:2]) in CODIGOS_UF:
            saida[cod] = n
        # "Ignorado/exterior" entra só no Total (ver DECISIONS.md).
    faltando = (CODIGOS_UF | {BR}) - set(saida)
    if faltando:
        raise ValueError(f"TabNet {ano}: geografias ausentes {sorted(faltando)}")
    return saida
