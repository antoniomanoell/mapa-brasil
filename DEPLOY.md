# DEPLOY.md — publicação no Cloudflare Pages

O site é estático. O build do frontend lê os dados já publicados em `data/public/` (versionados no git);
o pipeline **não** roda no deploy. Atualizar dados = rodar o pipeline localmente, revisar o diff e
fazer commit (PROJECT.md, 6.3).

## Configuração única (no painel do Cloudflare, feita pelo mantenedor)

1. Cloudflare → **Workers & Pages** → **Create** → **Pages** → **Connect to Git** → repositório
   `antoniomanoell/mapa-brasil`, branch de produção `main`.
2. Build settings:
   - **Framework preset:** None
   - **Build command:** `npm ci --prefix web && npm run build --prefix web`
   - **Build output directory:** `web/dist`
   - **Root directory:** `/` (raiz do repositório)
3. Variáveis de ambiente (Production e Preview):
   - `NODE_VERSION` = `24`
   - `VITE_SITE_URL` = URL pública do site, sem barra no fim (ex.: `https://<projeto>.pages.dev`
     ou o domínio próprio). Usada na imagem de compartilhamento (`og:image`).
   - `VITE_CF_BEACON_TOKEN` (opcional) = token do **Cloudflare Web Analytics** (Analytics & Logs →
     Web Analytics → Add a site). Vazio = sem analytics. Não usa cookies.
4. Salvar e fazer o primeiro deploy. Cada push na `main` publica de novo; cada PR ganha uma prévia.

O arquivo `web/public/_headers` define o cache: assets com hash ficam em cache permanente; catálogo
e indicadores, por 1 hora; a malha, por 1 dia.

## Antes do primeiro deploy

- [ ] Trocar `VITE_SITE_URL` em `web/.env` (padrão local) pela URL definitiva.
- [ ] Revisar os textos marcados com `<!-- REVISAR -->` em `web/src/content/` (enquanto a marca
      existir, a página mostra o aviso "Rascunho").
- [ ] Revisar os alertas de `pipeline/REPORT.md`.

## Conferir depois do deploy

- Abrir o site no celular e no computador; trocar indicador, ano e estado; abrir "Sobre o
  indicador".
- Testar o link compartilhado (a URL guarda indicador, ano, estado e visão).
- Rodar o Lighthouse (aba Lighthouse do Chrome DevTools, modo celular): a meta do projeto é ≥ 90 em
  desempenho e acessibilidade.
