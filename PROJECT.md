# PROJECT.md — Mapa de Indicadores Socioeconômicos do Brasil

> Nome provisório do projeto: **Indicadores BR**. Não usar "Atlas" no nome (conflita com o Atlas Brasil do PNUD/IPEA/FJP).

## 1. Objetivo

Site público, gratuito e em português que mostra, num mapa interativo do Brasil por estado (UF), a evolução de indicadores socioeconômicos de 2000 até o dado mais recente, usando exclusivamente fontes oficiais.

O objetivo do produto é mostrar fatos e dados ao maior número possível de pessoas. Por isso o site tem que ser:

- **Confiável:** cada número rastreável até a fonte oficial.
- **Honesto:** quebras metodológicas visíveis, nunca escondidas.
- **Compreensível para leigos:** cada indicador explicado em linguagem simples.
- **Leve e rápido:** funciona bem no celular com conexão ruim.

## 2. Princípios inegociáveis (ler antes de qualquer código)

1. **Nenhum número sem fonte.** Todo valor exibido vem de uma fonte oficial identificada. Cada indicador registra fonte, tabela ou série, URL e data de extração.
2. **Nunca emendar séries de metodologias diferentes.** Onde houver quebra (ex.: PNAD → PNAD Contínua; IDHM do Censo → IDHM da PNAD Contínua), os dados são armazenados e exibidos como **segmentos distintos**:
   - No gráfico, cada segmento é uma linha separada, com a quebra marcada e explicada.
   - No mapa, o slider indica qual segmento ou fonte vale naquele ano.
   - Sobreposições (ex.: 2012–2015, com PNAD e PNADC) mostram os dois valores, sem média nem escolha silenciosa.
3. **Lacunas são lacunas.** Ano sem dado fica vazio, com cinza e hachura no mapa e quebra na linha do gráfico. Proibido interpolar, imputar ou repetir o último valor.
4. **Nada de projeções futuras.** Fontes que trazem projeção (ex.: projeções de população do IBGE) são cortadas no último ano já transcorrido. Valores modelados (não medidos diretamente) são rotulados como "estimativa".
5. **Valores monetários sempre reais (deflacionados)**, com ano-base explícito na interface.
6. **Neutralidade editorial.** O site não comenta, não atribui causas e não marca períodos de governos. Os textos explicam o que o indicador mede e suas limitações, não o que "significa politicamente".
7. **Incerteza à vista.** Indicadores de pesquisa amostral (PNAD/PNADC) trazem coeficiente de variação ou intervalo de confiança quando o IBGE publicar. Estimativas com CV alto (comum em UFs pequenas, como RR e AP) recebem marca visual de baixa precisão.

## 3. Escopo do MVP

### Dentro

- Mapa coroplético das 27 UFs.
- Seletor de indicador (13 indicadores, ver seção 4).
- Slider temporal (2000 → ano mais recente disponível do indicador), com botão de animação play/pause.
- Clique numa UF → painel com gráfico da série temporal daquela UF, com a linha do Brasil como referência.
- Link compartilhável: o estado da tela (indicador, ano, UF selecionada) fica codificado na URL.
- Visualização alternativa em **tabela/ranking ordenado** do ano selecionado. Serve a duas coisas:
  - Acessibilidade.
  - Contrapeso ao viés de área do mapa, em que estados grandes e pouco povoados dominam visualmente.
- Página "Sobre o indicador" para cada um: o que mede, como ler, fonte(s), quebras, limitações, link para a fonte original.
- Página "Metodologia geral" e "Sobre o projeto".
- Responsivo, priorizando o celular.

### Fora do MVP (fases futuras, não implementar agora)

- Nível municipal (fase futura prevista; a arquitetura deve permitir, ver seção 7).
- Download de dados (CSV).
- Comparação lado a lado de várias UFs.
- Desagregações por sexo e raça/cor.
- Versão em inglês.
- Atualização automática agendada (o pipeline roda manualmente).

## 4. Catálogo de indicadores (MVP — todos os 13)

Legenda:

- **[confirmar]** = o Claude Code deve verificar na fonte e registrar o valor real no catálogo. **Não assumir** o valor escrito aqui.
- "Segmento" = trecho da série com metodologia homogênea.

| # | id | Indicador | Fonte(s) | Segmentos esperados | Unidade | Maior é |
|---|---|---|---|---|---|---|
| 1 | `idhm` | IDHM (geral + Longevidade, Educação, Renda) | PNUD/IPEA/FJP | A: Censo — 2000, 2010 · B: PNADC — 2012–2024 [confirmar fim] | índice 0–1 | melhor |
| 2 | `renda_pc` | Renda domiciliar per capita média, real | IBGE (PNAD; PNADC) | A: PNAD 2001–2015 · B: PNADC 2012+ | R$ do ano-base | melhor |
| 3 | `pobreza` | % da população abaixo da linha de pobreza (US$ 6,85 PPC/dia) | IBGE – Síntese de Indicadores Sociais | A: PNADC 2012+ | % | pior |
| 4 | `extrema_pobreza` | % da população abaixo da linha de extrema pobreza (US$ 2,15 PPC/dia) | IBGE – SIS | A: PNADC 2012+ | % | pior |
| 5 | `gini` | Índice de Gini da renda domiciliar per capita | IBGE (PNAD; PNADC) | A: PNAD 2001–2015 · B: PNADC 2012+ | índice 0–1 | pior |
| 6 | `desocupacao` | Taxa de desocupação | IBGE – PNADC | A: PNADC 2012+ (média anual dos trimestres ou dado anual oficial [confirmar qual o IBGE publica]) | % | pior |
| 7 | `informalidade` | Taxa de informalidade | IBGE – PNADC | A: PNADC [confirmar início, provável 2016] | % | pior |
| 8 | `pib_pc` | PIB per capita real | IBGE – Contas Regionais | A: série de referência vigente [confirmar ano inicial, provável 2002] | R$ do ano-base | melhor |
| 9 | `esperanca_vida` | Esperança de vida ao nascer | IBGE – Projeções da População (revisão mais recente) | A: 2000 → último ano transcorrido | anos | melhor |
| 10 | `mort_infantil` | Taxa de mortalidade infantil (óbitos < 1 ano por mil nascidos vivos) | IBGE – Projeções (principal); DATASUS SIM/SINASC (referência) | A: 2000 → último ano transcorrido | por mil NV | pior |
| 11 | `homicidios` | Taxa de homicídios por 100 mil hab. | DATASUS – SIM (óbitos por residência) + população IBGE | A: 2000 → último ano consolidado do SIM | por 100 mil | pior |
| 12 | `analfabetismo` | Taxa de analfabetismo, 15 anos ou mais | IBGE (PNAD; PNADC) | A: PNAD 2001–2015 · B: PNADC [confirmar início, provável 2016] | % | pior |
| 13 | `ideb` | IDEB — anos iniciais, anos finais, ensino médio (rede pública) | INEP | A: 2005+, bienal | índice 0–10 | melhor |
| 14* | `esgoto` | % de domicílios com esgotamento sanitário adequado (rede geral ou fossa séptica ligada à rede [confirmar definição oficial]) | IBGE (PNAD; PNADC) | A: PNAD 2001–2015 · B: PNADC [confirmar, provável 2016+] | % | melhor |

\* São 13 temas. Pobreza e extrema pobreza contam como um tema com dois indicadores irmãos, e o IDEB é um indicador com 3 etapas (subseletor no painel). Todos entram no MVP.

### 4.1 Regras específicas por indicador

**Geral — anos de Censo na PNAD antiga.** A PNAD anual **não foi a campo em 2000 nem em 2010** (anos de Censo). Esses anos ficam como lacuna nos segmentos PNAD. Não preencher com dado do Censo, que é outra fonte.

**Geral — PNAD 2001–2003 na região Norte.** Até 2003 a PNAD **não cobria a área rural** de RO, AC, AM, RR, PA e AP (cobertura total a partir de 2004). Para esses 6 estados, os valores de 2001–2003 do segmento PNAD recebem marca "cobertura apenas urbana — não comparável", visível no gráfico, no tooltip e na tabela. [confirmar a lista exata de UFs na documentação da PNAD]

**`idhm`**
- O segmento A vem dos dados censitários do Atlas Brasil. O segmento B vem do Radar IDHM (PNADC).
- Pode haver anos em que o PNUD não calculou o IDHM geral, por limitação de dados durante a pandemia. Respeitar a lacuna.
- Guardar também as três dimensões, para o painel.

**`renda_pc`**
- Deflacionar pelo IPCA para reais do último ano disponível. Registrar o ano-base no metadado e mostrar na legenda.
- Atenção à diferença de conceito de renda entre PNAD e PNADC, que é mais um motivo para não emendar.

**`pobreza` / `extrema_pobreza`**
- Usar exatamente a série publicada pelo IBGE na SIS (linhas do Banco Mundial em PPC).
- **Não** misturar com séries de pobreza do Ipeadata, que usam outras linhas.
- As tabelas da SIS podem estar só em planilhas no site do IBGE. Nesse caso, ver seção 6.2 (entradas manuais).

**`desocupacao`**
- A PNAD anual antiga usava conceito diferente de desocupação. **Não** criar segmento PNAD para este indicador; a série começa em 2012.

**`pib_pc`**
- PIB real **não** deve ser deflacionado pelo IPCA.
- Construir o PIB real a partir do índice de volume encadeado das Contas Regionais, a preços do último ano.
- Dividir pela mesma série de população usada nos demais indicadores (ver 4.2).
- Não emendar com séries de referência anteriores das Contas Regionais.

**`mort_infantil`**
- Indicador principal: a estimativa do IBGE (corrige o sub-registro de óbitos).
- A taxa direta do DATASUS (óbitos SIM < 1 ano ÷ nascidos vivos SINASC × 1000) fica como série de referência no painel, com nota: no início dos anos 2000 o sub-registro, maior no Norte e no Nordeste, faz a taxa direta **subestimar** a mortalidade justamente nos estados mais pobres.

**`homicidios`**
- Definição alinhada ao Atlas da Violência (IPEA): óbitos por agressão (CID-10 X85–Y09) + intervenção legal (Y35–Y36), por UF de residência [confirmar a definição atual usada pelo IPEA e registrar].
- Usar apenas anos com o SIM consolidado (não usar dados preliminares).

**`ideb`**
- Rede pública, as três etapas.
- Anos sem IDEB (ímpares) são lacunas. No gráfico, os pontos bienais são ligados apenas visualmente (linha tracejada entre pontos) e o tooltip deixa claro que não há dado no meio.

**`esperanca_vida` / `mort_infantil` (projeções IBGE)**
- Usar a revisão mais recente das Projeções da População (pós-Censo 2022), que reestima a série desde 2000.
- Cortar no último ano transcorrido.
- Rotular como "estimativa IBGE".

### 4.2 Denominador populacional único

Todas as taxas calculadas pelo projeto (homicídios, PIB per capita) usam **uma única série de população por UF**: a revisão mais recente das Projeções da População do IBGE, que é consistente de 2000 em diante. As estimativas anuais antigas do TCU têm saltos nos anos de Censo e não devem ser usadas.

## 5. Arquitetura

Site **estático, sem backend**. Os dados são pré-processados por um pipeline Python e publicados como arquivos JSON versionados. O custo de hospedagem deve ser zero ou próximo de zero.

```
[Fontes oficiais] → pipeline Python (manual) → data/public/*.json → site estático (Vite + TS) → CDN
```

### 5.1 Stack

| Camada | Escolha | Motivo |
|---|---|---|
| Pipeline | Python 3.12, `uv`, `polars` (ou pandas), `httpx`, `pydantic`, `pytest` | Ecossistema de dados maduro |
| Frontend | Vite + **TypeScript, sem framework de UI** (DOM + pequeno store próprio) | Superfície pequena (mapa, slider, painel, tabela); manutenção simples por quem conhece TS; bundle mínimo |
| Mapa | MapLibre GL JS **sem mapa-base** (só os polígonos das UFs, fundo neutro) | Escala para 5.570 municípios na fase futura sem reescrever (WebGL) |
| Gráficos | Observable Plot | Bons padrões de visualização, leve, ótimo para séries temporais com segmentos |
| Escalas de cor | d3-scale-chromatic (paletas sequenciais seguras para daltônicos, ex.: viridis/cividis ou ColorBrewer) | Acessibilidade |
| Testes front | Vitest (lógica: estado/URL, escalas) + Playwright (fumaça: carregar, trocar indicador, mover slider, clicar UF) | |
| Hospedagem | Cloudflare Pages (ou GitHub Pages) | Estático, grátis, CDN |
| Analytics | Cloudflare Web Analytics (sem cookies) — opcional | Privacidade |

### 5.2 Estrutura do repositório

```
/
├── PROJECT.md
├── pipeline/
│   ├── pyproject.toml
│   ├── src/indicadores/
│   │   ├── sources/          # um módulo por fonte (ibge_sidra.py, ipeadata.py, ibge_projecoes.py, datasus_sim.py, inep_ideb.py, atlas_idhm.py, ibge_sis.py, ibge_contas_regionais.py, ibge_malhas.py)
│   │   ├── indicators/       # um módulo por indicador: busca → transforma → valida → emite
│   │   ├── deflate.py        # IPCA, índices de volume
│   │   ├── population.py     # série única de população (4.2)
│   │   ├── schema.py         # modelos pydantic do formato publicado
│   │   ├── validate.py       # checagens (seção 8)
│   │   └── cli.py            # `uv run indicadores build [--only id]`
│   ├── raw_manual/           # arquivos baixados à mão quando não há API (com MANIFEST.yaml: URL, data, sha256)
│   ├── cache/                # respostas brutas das APIs (gitignored)
│   └── tests/
├── data/public/              # SAÍDA do pipeline, commitada no git (é o que o site consome)
│   ├── catalog.json
│   ├── indicators/<id>.json
│   └── geo/uf.topojson
└── web/
    ├── index.html
    ├── src/
    │   ├── main.ts
    │   ├── state.ts          # store + sincronização com URL
    │   ├── map.ts
    │   ├── slider.ts
    │   ├── panel.ts          # gráfico da UF
    │   ├── table.ts          # ranking/tabela
    │   ├── legend.ts
    │   └── content/          # textos "Sobre o indicador" em Markdown
    └── tests/
```

## 6. Pipeline de dados

### 6.1 Ordem de preferência de fonte

1. API ou tabela oficial publicada pelo próprio produtor (API SIDRA do IBGE, `servicodados.ibge.gov.br`; INEP; DATASUS).
2. Série oficial redistribuída por órgão público (Ipeadata, API OData v4: `http://www.ipeadata.gov.br/api/odata4/`), **somente se** for idêntica à do produtor e isso estiver documentado.
3. Processamento de microdados, **apenas** se não houver tabela publicada. Exige script reprodutível e validação contra os números divulgados oficialmente.

Os códigos de tabelas SIDRA, séries Ipeadata e demais identificadores **devem ser descobertos e verificados** via metadados das próprias APIs e registrados no catálogo. Não confiar em códigos de memória.

### 6.2 Entradas manuais

Algumas fontes não têm API (ex.: planilhas da SIS, downloads do Atlas Brasil/Radar IDHM, IDEB do INEP).

- Os arquivos vão em `pipeline/raw_manual/<fonte>/`.
- `MANIFEST.yaml` registra URL de origem, data de download e sha256 de cada arquivo.
- O pipeline falha se o hash não bater ou se faltar arquivo, com mensagem dizendo exatamente o que baixar e de onde.

### 6.3 Execução

- `uv run indicadores build` reconstrói tudo; `--only <id>` reconstrói um indicador.
- O pipeline é idempotente.
- Rodado manualmente pelo mantenedor. O resultado em `data/public/` é revisado no diff do git antes do commit.
- Ao final, gera `pipeline/REPORT.md` com, para cada indicador:
  - anos cobertos e segmentos;
  - lacunas;
  - alertas de validação;
  - variações ano a ano suspeitas;
  - comparação Brasil vs. valor nacional publicado.

### 6.4 Malha geográfica

- Malha das UFs da API de malhas do IBGE, simplificada e convertida para TopoJSON (alvo < 150 KB).
- Chave de junção: **código IBGE da UF (2 dígitos)**, nunca o nome ou a sigla.

## 7. Formato dos dados publicados

`data/public/catalog.json`: lista de indicadores com metadados resumidos (id, nome, tema, unidade, anos disponíveis), para montar o seletor sem baixar tudo.

`data/public/indicators/<id>.json`: carregado sob demanda.

```jsonc
{
  "id": "renda_pc",
  "nome": "Renda domiciliar per capita média",
  "tema": "Renda",
  "unidade": "R$",
  "unidade_detalhe": "R$ de 2024 (deflacionado pelo IPCA)",
  "direcao": "maior_melhor",          // ou "menor_melhor"
  "casas_decimais": 0,
  "tipo_valor": "medido",             // ou "estimativa"
  "subindicadores": null,             // ex.: IDEB → ["anos_iniciais","anos_finais","medio"]
  "segmentos": [
    {
      "id": "pnad",
      "rotulo": "PNAD (2001–2015)",
      "fonte": "IBGE – PNAD",
      "fonte_url": "https://...",
      "tabela": "<código verificado>",
      "extraido_em": "2026-10-20",
      "notas": "Sem dados em 2010 (ano de Censo). ...",
      "valores": {
        "28": { "2001": { "v": 512.3, "cv": 3.1, "flags": [] }, "...": {} },
        "BR": { "2001": { "v": 801.2 } }
      }
    },
    { "id": "pnadc", "rotulo": "PNAD Contínua (2012–)", "...": "..." }
  ],
  "quebras": [
    { "ano": 2012, "texto": "Mudança de pesquisa: PNAD → PNAD Contínua. As séries não são diretamente comparáveis." }
  ],
  "escala": { "tipo": "quantil", "limites": [ ... ] },
  "versao_pipeline": "<git sha>"
}
```

Regras do formato:

- Chaves geográficas = código IBGE (`"28"` = SE) + `"BR"` para o total nacional.
- `flags` possíveis:
  - `"baixa_precisao"` (CV acima do limiar definido por indicador; padrão 15%);
  - `"cobertura_urbana"` (PNAD Norte 2001–2003);
  - `"estimativa"`;
  - `"preliminar"` (proibido publicar; existe só para o validador).
- A estrutura deve aceitar códigos de município de 7 dígitos sem mudança de schema (fase futura).

## 8. Validação (o pipeline falha se algo não passar)

1. **Schema:** todo JSON valida contra os modelos pydantic.
2. **Cobertura:** as 27 UFs + BR presentes em todo ano declarado do segmento, ou a ausência registrada como lacuna explícita.
3. **Faixas plausíveis:** limites por indicador (ex.: % entre 0 e 100; Gini entre 0 e 1; IDEB entre 0 e 10).
4. **Variação suspeita:** variação ano a ano acima de um limiar por indicador gera **alerta** no REPORT (não falha), para revisão humana.
5. **Conferência com números publicados:** para cada indicador, ao menos 3 valores (incluindo o Brasil no ano mais recente) comparados com o valor divulgado pela fonte, com tolerância de arredondamento. Os valores de referência ficam em `pipeline/tests/fixtures/referencias.yaml` com a URL de onde vieram.
6. **Sem projeções:** nenhum ano posterior ao último ano transcorrido.
7. **Sem emenda:** nenhum segmento cobre anos de duas metodologias.

## 9. Interface

### 9.1 Layout (prioridade para o celular)

- **Topo:** seletor de indicador agrupado por tema, com subseletor quando houver (IDEB: etapa; IDHM: geral ou dimensão).
- **Centro:** mapa. Ao lado (desktop) ou abaixo (celular): alternância **Mapa | Ranking**.
- **Abaixo do mapa:** slider temporal com play/pause.
  - Mostra o ano e o rótulo do segmento vigente (ex.: "2014 · PNAD").
  - Nos anos com dois segmentos (sobreposição), permite alternar o segmento exibido no mapa.
  - Padrão: o segmento mais recente.
- **Painel da UF** (gaveta lateral no desktop, folha inferior no celular), ao clicar ou tocar num estado:
  - gráfico da série, com segmentos separados e a linha do Brasil em cinza;
  - quebras marcadas com linha vertical e ícone de informação;
  - pontos com flag desenhados de forma diferente (vazados/hachurados), com explicação no tooltip.
- **Rodapé de cada visualização:** fonte, ano-base (se monetário), link "Sobre este indicador".

### 9.2 Regras de visualização

- **Escala de cor fixa ao longo do tempo:** limites calculados uma vez sobre todos os anos do indicador (agregando os segmentos), **não** recalculados a cada ano. Assim a mudança de cor no slider reflete mudança real.
  - Padrão: 5 classes por quantis do conjunto agregado.
  - A legenda mostra os limites numéricos e a direção ("mais escuro = maior").
- Paleta sequencial de um matiz, segura para daltônicos. Nada de vermelho/verde.
- Sem dado = cinza com hachura, com "sem dado" na legenda.
- O tooltip no mapa mostra UF, valor formatado em pt-BR (vírgula decimal), ano, segmento e flags.
- O ranking mostra o ano selecionado, ordenado, com barra horizontal e o Brasil como linha de referência.

### 9.3 Estado na URL

Formato: `?i=<id>&s=<subindicador>&a=<ano>&g=<segmento>&uf=<sigla>&v=<mapa|ranking>`

- Toda mudança de estado atualiza a URL (`history.replaceState`).
- Abrir a URL restaura exatamente a tela.
- Parâmetros inválidos caem para os padrões sem quebrar.
- Cada estado gera `<title>` e meta description adequados. Imagem Open Graph genérica do projeto no MVP; imagem por estado fica para fase futura.

### 9.4 Textos para o público

Para cada indicador, um arquivo Markdown em `web/src/content/<id>.md` com as seções:

- O que mede
- Como ler
- De onde vem
- Mudanças de metodologia
- Limitações

Linguagem simples, frases curtas, sem jargão sem explicação.

**Todos os textos gerados pelo Claude Code são rascunhos** e devem ser marcados com `<!-- REVISAR -->` até a revisão humana do mantenedor.

### 9.5 Acessibilidade e desempenho

- Navegação completa por teclado (seletor, slider, UFs, painel); a tabela/ranking é a alternativa acessível ao mapa.
- Contraste AA.
- Carregamento inicial (HTML + JS + CSS + malha + catálogo + 1 indicador) < 500 KB comprimido; demais indicadores sob demanda.
- Lighthouse ≥ 90 em desempenho e acessibilidade no celular.

## 10. Fases de construção

**Fase 0 — Fundação**
- Repositório, estrutura de pastas, `uv`, Vite + TS, lint/format, CI rodando `pytest` e `vitest`.

**Fase 1 — Pipeline ponta a ponta com 3 indicadores-piloto**
- `homicidios` (cálculo próprio + população), `idhm` (dois segmentos + entrada manual) e `renda_pc` (dois segmentos + deflação).
- Malha das UFs, catálogo, validação completa, REPORT.md.
- *Critério de pronto:* os três passam na conferência com números publicados.

**Fase 2 — Frontend núcleo**
- Mapa, seletor, slider com play, painel da UF com segmentos e quebras, ranking, estado na URL, usando os 3 pilotos.
- *Critério de pronto:* testes Playwright de fumaça passando; uso confortável no celular.

**Fase 3 — Demais indicadores**
- Os 10 restantes, um a um, cada um com validação e REPORT.
- Resolver todos os itens **[confirmar]** e atualizar a tabela da seção 4 deste arquivo com os valores reais encontrados.

**Fase 4 — Conteúdo e publicação**
- Textos "Sobre o indicador" (rascunhos marcados para revisão), páginas Metodologia e Sobre, meta tags, deploy no Cloudflare Pages, analytics.

**Fase futura — Municípios** (não iniciar sem novo planejamento)
- Exige tratar:
  - indicadores só censitários;
  - municípios criados após 2000;
  - instabilidade de taxas em municípios pequenos (suavização ou marcação; ver Gelman & Price, 1999).

## 11. Regras de trabalho para o Claude Code

- Em caso de dúvida metodológica (qual tabela, qual definição, se dois segmentos são comparáveis), **parar e perguntar** ao mantenedor. Não decidir sozinho por conveniência técnica.
- Nunca inventar código de tabela, URL ou número. Se a fonte estiver fora do ar ou mudou, registrar no REPORT e perguntar.
- Toda decisão metodológica tomada vai para `DECISIONS.md` (data, decisão, motivo, fonte).
- Commits pequenos, por indicador ou funcionalidade.

## 12. Referências conceituais

- Gelman, A. & Price, P. N. (1999). *All maps of parameter estimates are misleading*. Statistics in Medicine. → instabilidade de taxas em áreas pequenas (relevante na fase municipal).
- Monmonier, M. *How to Lie with Maps*. → classificação de cores, viés de área.
- Cairo, A. *How Charts Lie*. → escalas, quebras, honestidade visual.
- Documentação metodológica do IBGE (PNAD, PNAD Contínua, SIS, Contas Regionais, Projeções da População), do PNUD/IPEA/FJP (Atlas Brasil e Radar IDHM), do INEP (IDEB) e do IPEA (Atlas da Violência).
