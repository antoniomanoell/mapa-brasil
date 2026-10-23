# DEPLOY.md — publicação na Vercel (site estático)

O site é estático. O build do frontend lê os dados já publicados em `data/public/` (versionados no git);
o pipeline **não** roda no deploy. Atualizar dados = rodar o pipeline localmente, revisar o diff e
fazer commit (PROJECT.md, 6.3).

A publicação usa a **Vercel** (ver DECISIONS.md, 2026-10-23; antes era o Cloudflare Workers). A
configuração fica em `vercel.json`, na raiz: comandos de instalação e build, pasta publicada
(`web/dist`), URLs sem `.html` e cabeçalhos de cache.

## Configuração única (no painel da Vercel, feita pelo mantenedor)

1. Vercel → **Add New… → Project** → **Import Git Repository** → autorizar o GitHub e escolher
   `antoniomanoell/mapa-brasil`.
2. Configuração do projeto:
   - **Project name:** `indicadores-br` (vira o endereço `indicadores-br.vercel.app`, se o nome
     estiver livre; senão, escolher outro curto)
   - **Framework Preset:** Other
   - **Root Directory:** `./` (raiz do repositório; os comandos e a pasta de saída vêm do
     `vercel.json`, não precisa preencher)
3. Settings → **General → Node.js Version:** 24.x.
4. Settings → **Environment Variables** (ambiente Production e Preview):
   - `VITE_SITE_URL` = URL pública do site, sem barra no fim (ex.: `https://indicadores-br.vercel.app`
     ou o domínio próprio). Usada na imagem de compartilhamento (`og:image`).
   - `VITE_CF_BEACON_TOKEN` (opcional) = token do Cloudflare Web Analytics, que funciona em qualquer
     domínio. Vazio = sem analytics. Não usa cookies.
5. **Deploy.** Cada push na `main` publica de novo; as outras branches e os PRs ganham uma URL de
   prévia.
6. Domínio próprio (opcional): Settings → **Domains** → adicionar o domínio e seguir as instruções de
   DNS. Depois, atualizar `VITE_SITE_URL`.

Os nomes dos botões do painel mudam com o tempo; o essencial é: projeto ligado ao repositório, o
`vercel.json` na raiz, Node 24 e as variáveis de build.

O `vercel.json` define o cache: assets com hash ficam em cache permanente; catálogo e indicadores,
por 1 hora; a malha, por 1 dia. Com `cleanUrls`, os links `pagina.html` são redirecionados para
`/pagina`, mantendo os parâmetros da URL. O `web/public/_headers` é o equivalente para o Cloudflare
e é ignorado pela Vercel.

## Testar localmente

```bash
npm run build --prefix web
npm run preview --prefix web
```

## Saída do Cloudflare

Enquanto o projeto do Cloudflare continuar ligado ao repositório, cada push publica nos dois. Depois
de conferir o site na Vercel: Cloudflare → Workers & Pages → `indicadores-br` → Settings → desligar o
build automático (ou apagar o projeto), e então remover `wrangler.jsonc` e `web/public/_headers`.

## Antes do primeiro deploy

- [x] Trocar `VITE_SITE_URL` em `web/.env` (padrão local) pela URL definitiva.
- [x] Revisar os textos marcados com `<!-- REVISAR -->` em `web/src/content/` (enquanto a marca
      existir, a página mostra o aviso "Rascunho").
- [x] Revisar os alertas de `pipeline/REPORT.md` (resultado em `pipeline/REVISAO_ALERTAS.md`).

## Conferir depois do deploy

- Abrir o site no celular e no computador; trocar indicador, ano e estado; abrir "Sobre o
  indicador".
- Testar o link compartilhado (a URL guarda indicador, ano, estado e visão).
- Conferir os cabeçalhos: `curl -I <url>/catalog.json` deve mostrar `Cache-Control: public, max-age=3600`.
- Rodar o Lighthouse (aba Lighthouse do Chrome DevTools, modo celular): a meta do projeto é ≥ 90 em
  desempenho e acessibilidade.

## Manutenção da seção "Quem é responsável"

- Uma vez por ano, ou quando houver emenda constitucional ou lei relevante para uma área, reconferir
  os artigos listados em `web/src/content/competencias/FONTES.md` no texto vigente do Planalto
  (atenção às redações antigas repetidas sem tachado) e atualizar as datas de conferência.
