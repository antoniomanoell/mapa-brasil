# DEPLOY.md — publicação no Cloudflare (Workers com arquivos estáticos)

O site é estático. O build do frontend lê os dados já publicados em `data/public/` (versionados no git);
o pipeline **não** roda no deploy. Atualizar dados = rodar o pipeline localmente, revisar o diff e
fazer commit (PROJECT.md, 6.3).

A publicação usa **Workers com arquivos estáticos** (sem código de servidor), que a Cloudflare indica
para projetos novos no lugar do Pages (ver DECISIONS.md). A configuração fica em `wrangler.jsonc`, na
raiz: nome do projeto e pasta publicada (`web/dist`).

## Configuração única (no painel do Cloudflare, feita pelo mantenedor)

1. Cloudflare → **Workers & Pages** → **Create application** → **Import a repository** (ou
   "Continue with GitHub") → autorizar o GitHub e escolher `antoniomanoell/mapa-brasil`.
2. Configuração do projeto:
   - **Project name:** `indicadores-br` (precisa ser igual ao `name` do `wrangler.jsonc`)
   - **Build command:** `npm ci --prefix web && npm run build --prefix web`
   - **Deploy command:** `npx wrangler deploy` (o padrão)
   - **Non-production branch deploy command:** `npx wrangler versions upload` (o padrão; gera a
     prévia de cada branch)
   - **Path / Root directory:** `/` (raiz do repositório)
   - **Production branch:** `main`
3. Variáveis **de build** (Settings → Build → Variables and secrets; não confundir com as variáveis
   de runtime do Worker, que este site não usa):
   - `NODE_VERSION` = `24`
   - `VITE_SITE_URL` = URL pública do site, sem barra no fim (ex.:
     `https://indicadores-br.<sua-conta>.workers.dev` ou o domínio próprio). Usada na imagem de
     compartilhamento (`og:image`).
   - `VITE_CF_BEACON_TOKEN` (opcional) = token do **Cloudflare Web Analytics** (Analytics & Logs →
     Web Analytics → Add a site). Vazio = sem analytics. Não usa cookies.
4. Salvar e fazer o primeiro deploy. Cada push na `main` publica de novo; as outras branches ganham
   uma URL de prévia.

Os nomes dos botões do painel mudam com o tempo; o essencial é: projeto ligado ao repositório, os
comandos acima e as variáveis de build.

O arquivo `web/public/_headers` define o cache: assets com hash ficam em cache permanente; catálogo
e indicadores, por 1 hora; a malha, por 1 dia. Os links `pagina.html` são redirecionados para
`/pagina`, mantendo os parâmetros da URL.

## Testar localmente como no Cloudflare

```bash
npm run build --prefix web
npx wrangler dev
```

## Antes do primeiro deploy

- [x] Trocar `VITE_SITE_URL` em `web/.env` (padrão local) pela URL definitiva.
- [x] Revisar os textos marcados com `<!-- REVISAR -->` em `web/src/content/` (enquanto a marca
      existir, a página mostra o aviso "Rascunho").
- [x] Revisar os alertas de `pipeline/REPORT.md` (resultado em `pipeline/REVISAO_ALERTAS.md`).

## Conferir depois do deploy

- Abrir o site no celular e no computador; trocar indicador, ano e estado; abrir "Sobre o
  indicador".
- Testar o link compartilhado (a URL guarda indicador, ano, estado e visão).
- Rodar o Lighthouse (aba Lighthouse do Chrome DevTools, modo celular): a meta do projeto é ≥ 90 em
  desempenho e acessibilidade.
