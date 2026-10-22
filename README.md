# Indicadores BR

Mapa interativo de indicadores socioeconômicos do Brasil por UF, de 2000 até o dado mais recente, usando só fontes oficiais.

A especificação completa está em [PROJECT.md](PROJECT.md). As decisões metodológicas ficam em [DECISIONS.md](DECISIONS.md), as fontes verificadas em [pipeline/FONTES.md](pipeline/FONTES.md) e a publicação está descrita em [DEPLOY.md](DEPLOY.md).

## Estrutura

- `pipeline/`: pipeline Python que busca, transforma e valida os dados.
- `data/public/`: saída do pipeline (JSON), versionada. É o que o site consome.
- `web/`: site estático (Vite + TypeScript).

## Pipeline

Requer [uv](https://docs.astral.sh/uv/).

```bash
cd pipeline
uv sync
uv run indicadores build            # reconstrói tudo
uv run indicadores build --only idhm
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

## Web

Requer Node 24.

```bash
cd web
npm install
npm run dev
npm test
npm run lint && npm run format:check && npm run typecheck
npx playwright test                 # testes de fumaça (desktop e celular)
```

Textos do site: `web/src/content/` (Markdown; `<!-- REVISAR -->` marca rascunho e mostra o aviso no site).

## Licença

Código: [MIT](LICENSE). Textos do site e dados derivados (`data/public/`): CC BY 4.0, ver
[LICENSE-CONTEUDO.md](LICENSE-CONTEUDO.md). Os dados originais seguem os termos de cada órgão produtor.
