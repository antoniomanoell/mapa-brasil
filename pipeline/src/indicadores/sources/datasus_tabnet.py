"""DATASUS — consultas ao TabNet (SIM, SINASC) por UF de residência (ver FONTES.md)."""

import html
import re
from datetime import date
from functools import cached_property
from urllib.parse import urlencode

from ..ufs import BR, CODIGOS_UF
from .http import requisitar

TODAS = "TODAS_AS_CATEGORIAS__"


class Tabnet:
    """Um formulário do TabNet (arquivo .def), consultado ano a ano com Linha = UF."""

    def __init__(self, def_: str, incremento: str, prefixo_arquivo: str) -> None:
        self.def_ = def_
        self.incremento = incremento
        self.prefixo_arquivo = prefixo_arquivo
        self.url_formulario = f"http://tabnet.datasus.gov.br/cgi/deftohtm.exe?{def_}"
        self.url_consulta = f"http://tabnet.datasus.gov.br/cgi/tabcgi.exe?{def_}"

    @cached_property
    def _formulario(self) -> str:
        return requisitar(self.url_formulario, usar_cache=False).conteudo.decode("latin-1")

    def anos_preliminares(self) -> list[int]:
        """Anos que o próprio formulário declara como preliminares."""
        anos = [
            int(a) for a in re.findall(r"Dados de (\d{4})\s*-\s*Preliminares", self._formulario)
        ]
        if not anos:
            raise ValueError(f"{self.def_}: sem aviso de anos preliminares — formulário mudou?")
        return anos

    def _filtros(self) -> list[str]:
        """Nomes de todos os filtros (selects "S…") do formulário, lidos do próprio HTML."""
        nomes = re.findall(r'<SELECT[^>]*NAME="(S[^"]+)"', self._formulario, re.I)
        if not nomes:
            raise ValueError(f"{self.def_}: formulário sem filtros — formato mudou?")
        return nomes

    def por_uf(
        self, ano: int, filtros: dict[str, list[str]] | None = None
    ) -> tuple[dict[str, int], date]:
        """Contagem por UF de residência em `ano` (mais "BR" = Total, que inclui ignorados)."""
        filtros = filtros or {}
        campos = [
            ("Linha", "Unidade_da_Federação"),
            ("Coluna", "--Não-Ativa--"),
            ("Incremento", self.incremento),
            ("Arquivos", f"{self.prefixo_arquivo}{ano % 100:02d}.dbf"),
        ]
        for nome in self._filtros():
            campos += [(nome, v) for v in filtros.get(nome, [TODAS])]
        campos += [("zeradas", "exibirlz"), ("formato", "prn"), ("mostre", "Mostra")]
        resp = requisitar(self.url_consulta, corpo=urlencode(campos, encoding="latin-1").encode())
        return ler_prn(resp.conteudo.decode("latin-1"), f"{self.def_} {ano}"), resp.obtido_em


def ler_prn(pagina: str, contexto: str) -> dict[str, int]:
    bloco = re.search(r"<PRE>(.*?)</PRE>", pagina, re.S | re.I)
    if not bloco:
        raise ValueError(f"TabNet {contexto}: resposta sem tabela")
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
        raise ValueError(f"TabNet {contexto}: geografias ausentes {sorted(faltando)}")
    return saida


# SIM: óbitos por residência. Códigos conferidos no formulário em 2026-10-20/21.
SIM = Tabnet("sim/cnv/obt10uf.def", "Óbitos_p/Residênc", "obtuf")
SIM_GRUPO_AGRESSOES = "246"  # X85–Y09
SIM_GRUPO_INTERVENCOES_LEGAIS = "248"  # Y35–Y36 (intervenções legais e operações de guerra)
SIM_FAIXA_MENOR_1_ANO = "1"  # SFaixa_Etária = "Menor 1 ano"

# SINASC: nascidos vivos por residência da mãe.
SINASC = Tabnet("sinasc/cnv/nvuf.def", "Nascim_p/resid.mãe", "nvuf")
