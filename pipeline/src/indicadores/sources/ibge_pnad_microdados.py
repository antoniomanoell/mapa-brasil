"""IBGE — microdados da PNAD anual 2001–2015 (FTP): renda per capita, Gini e analfabetismo.

O SIDRA não publica a renda domiciliar per capita média por UF para a PNAD anual (ver FONTES.md),
então ela é calculada dos microdados (PROJECT.md, 6.1, regra 3). Conceito (DECISIONS.md):

- rendimento domiciliar = V4614, que já exclui o rendimento de pensionistas, empregados domésticos
  e seus parentes e de menores de 10 anos;
- per capita = V4614 ÷ moradores com condição no domicílio (V0401) de 1 a 5, isto é, sem
  pensionistas, empregados domésticos e seus parentes;
- universo: moradores de domicílios particulares (V0201 = 1 ou 3) com rendimento declarado;
- média por pessoa, com o peso da pessoa (V4729), incluindo quem mora em domicílio sem rendimento.
  É o conceito da tabela SIDRA 7533 (PNAD Contínua).

Também calcula, só para conferência, o conceito da Síntese de Indicadores Sociais 2016 (Tabela
6.6): média por domicílio (peso V4611), sem os domicílios sem rendimento. O CV é estimado por
linearização de Taylor com os estratos (V4617) e as UPAs (V4618) do plano amostral.

O Gini (segmento PNAD de `gini`) usa a mesma renda per capita por pessoa. Para conferência, calcula
também o Gini da SIS 2016 (Tabela 6.3): rendimento mensal de todas as fontes (V4720) das pessoas de
15 anos ou mais com rendimento, ponderado por V4729.

A taxa de analfabetismo (segmento PNAD de `analfabetismo`) é a proporção, ponderada por V4729, das
pessoas de 15 anos ou mais (V8005) que não sabem ler e escrever (V0601 = 3) entre as que responderam
(V0601 = 1 ou 3), com todos os moradores, como na SIS 2016 (Tabela 4.15). O SIDRA só publica as
contagens por UF em milhares (tabela 271), arredondadas e com 2009 do DF incompleto (DECISIONS.md).

As posições das variáveis mudam a cada ano; são lidas do input SAS que o IBGE publica junto.
"""

import json
import re
import zipfile
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path

import polars as pl

from ..paths import CACHE
from ..raw_manual import carregar_manifest, exigir
from ..ufs import BR, CODIGOS_UF

URL_MICRODADOS = (
    "https://ftp.ibge.gov.br/Trabalho_e_Rendimento/"
    "Pesquisa_Nacional_por_Amostra_de_Domicilios_anual/microdados/"
)
# Ano → (zip com os dados, zip com o input SAS; None = o input vem no próprio zip dos dados).
ARQUIVOS: dict[int, tuple[str, str | None]] = {
    2001: ("ibge_pnad/PNAD_reponderado_2001.zip", None),
    2002: ("ibge_pnad/PNAD_reponderado_2002.zip", None),
    2003: ("ibge_pnad/PNAD_reponderado_2003_20150814.zip", None),
    2004: ("ibge_pnad/PNAD_reponderado_2004.zip", None),
    2005: ("ibge_pnad/PNAD_reponderado_2005.zip", None),
    2006: ("ibge_pnad/PNAD_reponderado_2006.zip", None),
    2007: ("ibge_pnad/PNAD_reponderado_2007_20150814.zip", None),
    2008: ("ibge_pnad/PNAD_reponderado_2008.zip", None),
    2009: ("ibge_pnad/PNAD_reponderado_2009_20171228.zip", None),
    2011: ("ibge_pnad/PNAD_reponderado_2011_20150814.zip", None),
    2012: ("ibge_pnad/PNAD_reponderado_2012_20150814.zip", None),
    2013: (
        "ibge_pnad/pnad2013_Dados_20170807.zip",
        "ibge_pnad/pnad2013_Dicionarios_e_input_20170807.zip",
    ),
    2014: (
        "ibge_pnad/pnad2014_Dados_20170323.zip",
        "ibge_pnad/pnad2014_Dicionarios_e_input_20170323.zip",
    ),
    2015: (
        "ibge_pnad/pnad2015_Dados_20170517.zip",
        "ibge_pnad/pnad2015_Dicionarios_e_input_20170517.zip",
    ),
}
ANOS = sorted(ARQUIVOS)

# Variáveis lidas, com os nomes alternativos usados em alguns anos (2001: STRAT e PSU).
VARIAVEIS = {
    "DOM": {
        "V0102": ["V0102"],
        "V0103": ["V0103"],
        "V0201": ["V0201"],
        "V4611": ["V4611"],
        "V4614": ["V4614"],
        "V4617": ["V4617", "STRAT"],
        "V4618": ["V4618", "PSU"],
    },
    "PES": {
        "V0102": ["V0102"],
        "V0103": ["V0103"],
        "V0401": ["V0401"],
        "V4729": ["V4729"],
        "V8005": ["V8005"],
        "V0601": ["V0601"],
    },
}
# Opcionais: rendimento per capita pronto (a partir de 2004), usado para conferir o cálculo, e
# rendimento de todas as fontes (ausente do layout de 2001), usado só na conferência do Gini da SIS.
VERIFICACAO = {"DOM": {"V4621": ["V4621"]}, "PES": {"V4720": ["V4720"]}}

SEM_DECLARACAO = 999_999_999_999
ESPECIE_PARTICULAR = ("1", "3")  # particular permanente e particular improvisado
NAO_SABE_LER = "3"
LEITURA_RESPONDIDA = ("1", "3")  # V0601: 1 = sabe ler e escrever, 3 = não sabe
CONDICAO_MORADOR = ("1", "2", "3", "4", "5")  # exclui 6, 7 e 8 (pensionista, empregados domésticos)

# Mudar quando o cálculo mudar, para invalidar o cache.
VERSAO_CALCULO = "3"
_INPUT = re.compile(r"@0*(\d+)\s+(\w+)\s+\$?\s*(\d+)\.")


@dataclass(frozen=True)
class Estimativa:
    media: float
    cv: float | None  # %


@dataclass(frozen=True)
class RendaAno:
    """Renda domiciliar per capita nominal (R$ de setembro do ano) por geo ("BR" ou UF)."""

    ano: int
    por_pessoa: dict[str, Estimativa]
    # Conceito da SIS 2016, Tabela 6.6: média por domicílio, sem os domicílios sem rendimento.
    por_domicilio_sis: dict[str, Estimativa]
    # Gini da renda per capita por pessoa (mesmo universo de `por_pessoa`).
    gini: dict[str, float]
    # Conceito da SIS 2016, Tabela 6.3 (só conferência): vazio se o ano não tem V4720.
    gini_individual_sis: dict[str, float]
    # Taxa de analfabetismo das pessoas de 15 anos ou mais (%), com CV.
    analfabetismo: dict[str, Estimativa]


def ler_layout(texto_input: str) -> dict[str, tuple[int, int]]:
    """Variável → (posição inicial, 1-based; largura), a partir do input SAS do IBGE."""
    return {
        m.group(2).upper(): (int(m.group(1)), int(m.group(3))) for m in _INPUT.finditer(texto_input)
    }


def _membro(zf: zipfile.ZipFile, padrao: str) -> str:
    achados = [n for n in zf.namelist() if re.search(padrao, n, re.I) and "STATUS" not in n.upper()]
    if len(achados) != 1:
        raise ValueError(f"{zf.filename}: esperado 1 arquivo para {padrao!r}, achados {achados}")
    return achados[0]


def _posicoes(
    layout: dict[str, tuple[int, int]], quer: dict[str, list[str]], obrigatorio: bool, onde: str
) -> dict[str, tuple[int, int]]:
    saida = {}
    for nome, alternativas in quer.items():
        achado = next((layout[a] for a in alternativas if a in layout), None)
        if achado is not None:
            saida[nome] = achado
        elif obrigatorio:
            raise ValueError(f"{onde}: variável {nome} ausente do input SAS")
    return saida


def _ler_fixo(conteudo: bytes, posicoes: dict[str, tuple[int, int]]) -> pl.DataFrame:
    linhas = pl.Series("l", conteudo.decode("latin-1").splitlines())
    return pl.DataFrame(
        {
            nome: linhas.str.slice(inicio - 1, largura).str.strip_chars()
            for nome, (inicio, largura) in posicoes.items()
        }
    )


def ler_ano(ano: int) -> tuple[pl.DataFrame, pl.DataFrame]:
    """(domicílios, pessoas) do ano, só com as colunas usadas, como texto."""
    dados, dicionario = ARQUIVOS[ano]
    zdados = zipfile.ZipFile(exigir(dados))
    zinput = zipfile.ZipFile(exigir(dicionario)) if dicionario else zdados
    saida = []
    for tipo in ("DOM", "PES"):
        nome_input = _membro(zinput, rf"input[ _]?{tipo}{ano}\.txt$")
        layout = ler_layout(zinput.read(nome_input).decode("latin-1"))
        onde = f"PNAD {ano} {tipo}"
        posicoes = _posicoes(layout, VARIAVEIS[tipo], True, onde)
        posicoes |= _posicoes(layout, VERIFICACAO.get(tipo, {}), False, onde)
        nome_dados = _membro(zdados, rf"dados/{tipo}{ano}\.txt$")
        saida.append(_ler_fixo(zdados.read(nome_dados), posicoes))
    return saida[0], saida[1]


def _montar(
    dom: pl.DataFrame, pes: pl.DataFrame
) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    """(domicilios com rpc, pessoas com rpc, upas) — o universo do conceito por pessoa."""
    num = pl.col
    dom = dom.with_columns(
        num("V0102").str.slice(0, 2).alias("uf"),
        num("V4611").cast(pl.Float64, strict=False).alias("peso_dom"),
        num("V4614").cast(pl.Float64, strict=False).alias("renda"),
        pl.concat_str(num("V4617"), num("V4618"), separator="-").alias("upa"),
    )
    moradores = (
        pes.filter(num("V0401").is_in(CONDICAO_MORADOR))
        .group_by("V0102", "V0103")
        .agg(pl.len().alias("n"))
    )
    domicilios = (
        dom.filter(num("V0201").is_in(ESPECIE_PARTICULAR))
        .join(moradores, on=["V0102", "V0103"], how="inner")
        .filter(num("renda").is_not_null() & (num("renda") != SEM_DECLARACAO))
        .with_columns((num("renda") / num("n")).alias("rpc"))
    )
    _conferir_per_capita(domicilios)

    pessoas = (
        pes.filter(num("V0401").is_in(CONDICAO_MORADOR))
        .with_columns(num("V4729").cast(pl.Float64, strict=False).alias("peso"))
        .join(
            domicilios.select("V0102", "V0103", "uf", "V4617", "upa", "rpc"), on=["V0102", "V0103"]
        )
    )
    # Todas as UPAs da amostra, com seu estrato: UPAs sem nenhum caso do domínio entram com zero.
    upas = dom.select("V4617", "upa").unique()
    return domicilios, pessoas, upas


def calcular(dom: pl.DataFrame, pes: pl.DataFrame) -> tuple[dict, dict]:
    """(por_pessoa, por_domicilio_sis): geo → Estimativa, a partir dos microdados de um ano."""
    num = pl.col
    domicilios, pessoas, upas = _montar(dom, pes)
    por_pessoa = _estimar(pessoas, "rpc", "peso", upas)
    sis = domicilios.filter(num("rpc") > 0)
    por_domicilio = _estimar(sis, "rpc", "peso_dom", upas)
    return por_pessoa, por_domicilio


def calcular_gini(dom: pl.DataFrame, pes: pl.DataFrame) -> tuple[dict, dict]:
    """(gini por pessoa, gini individual da SIS): geo → índice."""
    _, pessoas, _ = _montar(dom, pes)
    gini = _por_geo(pessoas, lambda d: gini_ponderado(d["rpc"], d["peso"]))
    if "V4720" not in pes.columns:
        return gini, {}
    renda = pl.col("V4720").cast(pl.Float64, strict=False)
    individuos = pes.with_columns(
        pl.col("V0102").str.slice(0, 2).alias("uf"),
        renda.alias("y"),
        pl.col("V4729").cast(pl.Float64, strict=False).alias("peso"),
        pl.col("V8005").cast(pl.Int64, strict=False).alias("idade"),
    ).filter((pl.col("idade") >= 15) & (pl.col("y") > 0) & (pl.col("y") != SEM_DECLARACAO))
    sis = _por_geo(individuos, lambda d: gini_ponderado(d["y"], d["peso"]))
    return gini, sis


def calcular_analfabetismo(dom: pl.DataFrame, pes: pl.DataFrame) -> dict[str, Estimativa]:
    """Taxa de analfabetismo (%) das pessoas de 15 anos ou mais: geo → Estimativa."""
    num = pl.col
    plano = dom.select(
        "V0102",
        "V0103",
        "V4617",
        pl.concat_str(num("V4617"), num("V4618"), separator="-").alias("upa"),
    )
    pessoas = (
        pes.with_columns(
            num("V0102").str.slice(0, 2).alias("uf"),
            num("V4729").cast(pl.Float64, strict=False).alias("peso"),
            num("V8005").cast(pl.Int64, strict=False).alias("idade"),
            (num("V0601") == NAO_SABE_LER).cast(pl.Float64).mul(100).alias("analfabeta"),
        )
        .filter((num("idade") >= 15) & num("V0601").is_in(LEITURA_RESPONDIDA))
        .join(plano, on=["V0102", "V0103"])
    )
    return _estimar(pessoas, "analfabeta", "peso", plano.select("V4617", "upa").unique())


def _por_geo(casos: pl.DataFrame, f: Callable[[pl.DataFrame], float]) -> dict[str, float]:
    return {
        geo: float(f(casos if geo == BR else casos.filter(pl.col("uf") == geo)))
        for geo in [BR, *sorted(CODIGOS_UF)]
    }


def gini_ponderado(y: pl.Series, w: pl.Series) -> float:
    """Gini com pesos amostrais: 1 − Σ (Pᵢ − Pᵢ₋₁)(Lᵢ + Lᵢ₋₁), com os casos em ordem de renda."""
    d = pl.DataFrame({"y": y, "w": w}).sort("y")
    pw = d["w"] / d["w"].sum()
    renda = d["y"] * d["w"]
    lc = renda.cum_sum() / renda.sum()
    lc_ant = lc.shift(1, fill_value=0.0)
    return float(1 - (pw * (lc + lc_ant)).sum())


def _conferir_per_capita(domicilios: pl.DataFrame) -> None:
    """Onde o IBGE já publica o per capita (V4621), o cálculo tem de reproduzi-lo."""
    if "V4621" not in domicilios.columns:
        return
    publicado = pl.col("V4621").cast(pl.Float64, strict=False)
    divergentes = domicilios.filter(
        publicado.is_not_null()
        & (publicado != SEM_DECLARACAO)
        & ((pl.col("rpc") - publicado).abs() > 1)
    )
    if divergentes.height:
        raise ValueError(
            f"{divergentes.height} domicílios com per capita diferente do V4621 do IBGE"
        )


def _estimar(casos: pl.DataFrame, y: str, w: str, upas: pl.DataFrame) -> dict[str, Estimativa]:
    saida = {}
    for geo in [BR, *sorted(CODIGOS_UF)]:
        dominio = casos if geo == BR else casos.filter(pl.col("uf") == geo)
        if dominio.height == 0:
            raise ValueError(f"sem casos para {geo}")
        saida[geo] = _media_com_cv(dominio, y, w, upas)
    return saida


def _media_com_cv(dominio: pl.DataFrame, y: str, w: str, upas: pl.DataFrame) -> Estimativa:
    """Média ponderada (razão) e CV por linearização de Taylor, UPAs com reposição no estrato.

    Estratos com uma só UPA não contribuem para a variância.
    """
    soma_w = dominio[w].sum()
    media = (dominio[y] * dominio[w]).sum() / soma_w
    z = (
        dominio.with_columns((pl.col(w) * (pl.col(y) - media) / soma_w).alias("z"))
        .group_by("upa")
        .agg(pl.col("z").sum())
    )
    estratos = dominio.select("V4617").unique()
    por_upa = (
        upas.join(estratos, on="V4617")
        .join(z, on="upa", how="left")
        .with_columns(pl.col("z").fill_null(0.0))
    )
    var = (
        por_upa.group_by("V4617")
        .agg(
            pl.len().alias("nh"),
            ((pl.col("z") - pl.col("z").mean()) ** 2).sum().alias("ss"),
        )
        .filter(pl.col("nh") > 1)
        .select((pl.col("nh") / (pl.col("nh") - 1) * pl.col("ss")).sum())
        .item()
    )
    return Estimativa(media=float(media), cv=float(var**0.5 / media * 100))


def _caminho_cache(ano: int) -> Path:
    return CACHE / f"pnad_renda_pc_{ano}_v{VERSAO_CALCULO}.json"


def renda_ano(ano: int) -> RendaAno:
    """Resultado do ano, com cache em disco (ler os microdados leva dezenas de segundos)."""
    manifest = carregar_manifest()
    chave = [manifest[a].sha256 for a in ARQUIVOS[ano] if a]
    cache = _caminho_cache(ano)
    if cache.exists():
        guardado = json.loads(cache.read_text(encoding="utf-8"))
        if guardado["chave"] == chave:
            return _de_json(guardado)
    dom, pes = ler_ano(ano)
    por_pessoa, sis = calcular(dom, pes)
    gini, gini_sis = calcular_gini(dom, pes)
    resultado = RendaAno(
        analfabetismo=calcular_analfabetismo(dom, pes),
        ano=ano,
        por_pessoa=por_pessoa,
        por_domicilio_sis=sis,
        gini=gini,
        gini_individual_sis=gini_sis,
    )
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps({"chave": chave, **asdict(resultado)}), encoding="utf-8")
    return resultado


def _de_json(d: dict) -> RendaAno:
    return RendaAno(
        ano=d["ano"],
        por_pessoa={g: Estimativa(**e) for g, e in d["por_pessoa"].items()},
        por_domicilio_sis={g: Estimativa(**e) for g, e in d["por_domicilio_sis"].items()},
        gini=d["gini"],
        gini_individual_sis=d["gini_individual_sis"],
        analfabetismo={g: Estimativa(**e) for g, e in d["analfabetismo"].items()},
    )
