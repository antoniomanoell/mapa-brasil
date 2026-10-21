"""Orquestra o build: indicadores → validação → data/public/ → REPORT.md."""

import subprocess
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from .indicators.base import DefinicaoIndicador
from .paths import PUBLIC, PUBLIC_INDICADORES, RAIZ, REFERENCIAS, REPORT, escrever
from .report import escrever_report
from .schema import Catalogo, Indicador, ItemCatalogo
from .sources import ibge_malhas
from .validate import Resultado, carregar_referencias, validar


@dataclass
class Execucao:
    hoje: date
    versao: str
    escopo: str
    resultados: dict[str, tuple[Indicador | None, Resultado]] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return all(r.ok for _, r in self.resultados.values())


# O que determina a saída do build. O REPORT.md e os dados publicados não entram.
ENTRADAS_DO_BUILD = [
    "pipeline/src",
    "pipeline/pyproject.toml",
    "pipeline/uv.lock",
    "pipeline/raw_manual/MANIFEST.yaml",
    "pipeline/tests/fixtures",
]


def versao_pipeline() -> str:
    try:
        sha = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=RAIZ,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        sujo = subprocess.run(
            ["git", "status", "--porcelain", "--", *ENTRADAS_DO_BUILD],
            cwd=RAIZ,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "desconhecida"
    return f"{sha}-dirty" if sujo else sha


def escrever_json(ind: Indicador, destino_dir: Path = PUBLIC_INDICADORES) -> Path:
    destino_dir.mkdir(parents=True, exist_ok=True)
    destino = destino_dir / f"{ind.id}.json"
    escrever(destino, ind.model_dump_json(exclude_defaults=True) + "\n")
    return destino


def item_catalogo(ind: Indicador) -> ItemCatalogo:
    anos = [
        int(a)
        for seg in ind.segmentos
        if seg.papel == "principal"
        for serie in seg.valores.values()
        for a, p in serie.items()
        if p.v is not None
    ]
    return ItemCatalogo(
        id=ind.id,
        nome=ind.nome,
        tema=ind.tema,
        unidade=ind.unidade,
        subindicadores=ind.subindicadores,
        ano_inicial=min(anos),
        ano_final=max(anos),
        arquivo=f"indicators/{ind.id}.json",
    )


def escrever_catalogo(hoje: date, versao: str, ordem: list[str], public: Path = PUBLIC) -> Path:
    """Remonta o catálogo a partir de todos os indicadores publicados em disco, na `ordem` dada."""
    itens = [
        item_catalogo(Indicador.model_validate_json(p.read_text(encoding="utf-8")))
        for p in (public / "indicators").glob("*.json")
    ]
    posicao = {id_: i for i, id_ in enumerate(ordem)}
    itens.sort(key=lambda it: (posicao.get(it.id, len(ordem)), it.id))
    cat = Catalogo(gerado_em=hoje, versao_pipeline=versao, indicadores=itens)
    destino = public / "catalog.json"
    escrever(destino, cat.model_dump_json(indent=2) + "\n")
    return destino


def executar(definicoes: dict[str, DefinicaoIndicador], only: str | None, hoje: date) -> Execucao:
    versao = versao_pipeline()
    alvo = {only: definicoes[only]} if only else definicoes
    exe = Execucao(hoje=hoje, versao=versao, escopo=f"--only {only}" if only else "completo")
    referencias = carregar_referencias(REFERENCIAS)

    if not only:
        ibge_malhas.construir()

    for id_, defn in alvo.items():
        try:
            ind = defn.construir(versao, hoje)
        except Exception as e:
            exe.resultados[id_] = (None, Resultado(erros=[f"falha ao construir: {e}"]))
            continue
        res = validar(ind, defn.regras, referencias, hoje, getattr(defn, "auxiliares", None))
        exe.resultados[id_] = (ind, res)
        # Só publica o que passou na validação.
        if res.ok:
            escrever_json(ind)

    escrever_catalogo(hoje, versao, list(definicoes))
    escrever_report(exe, REPORT)
    return exe
