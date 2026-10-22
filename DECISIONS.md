# DECISIONS.md

Registro das decisões metodológicas do projeto (ver PROJECT.md, seção 11).

Formato de cada entrada:

```
## AAAA-MM-DD — <título curto>
- **Decisão:** ...
- **Motivo:** ...
- **Fonte:** <URL ou documento>
```

---

## 2026-10-20 — População: revisão 2024 das Projeções, via FTP (não SIDRA)
- **Decisão:** a série única de população (seção 4.2) vem de `projecoes_2024_tab4_indicadores.xlsx`
  (coluna `POP_T`), cortada no último ano transcorrido.
- **Motivo:** as tabelas do SIDRA (7358/7360/7362) são da revisão 2018, e o PROJECT.md pede a revisão
  pós-Censo 2022. A planilha é publicação oficial do IBGE. Seu sha256 fica fixado no MANIFEST.
- **Fonte:** https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2024/

## 2026-10-20 — renda_pc: só PNAD Contínua na Fase 1
- **Decisão:** `renda_pc` sai com um único segmento PNADC (2012+). O segmento PNAD 2001–2015 fica para
  uma tarefa separada, por microdados (regra 3 da seção 6.1), validados contra números do IBGE.
- **Motivo:** o SIDRA não publica renda domiciliar per capita média por UF para a PNAD anual. A série
  do Ipeadata é cálculo próprio do IPEA e violaria a regra 2. Decidido pelo mantenedor.
- **Fonte:** catálogo de agregados do SIDRA (pesquisa `PD`), consultado em 2026-10-20.

## 2026-10-20 — renda_pc: série real deflacionada pelo IBGE
- **Decisão:** usar a tabela SIDRA 7533 ("a preços médios do último ano", com CV), em vez de deflacionar
  a série nominal pelo IPCA no próprio projeto. O ano-base é o último ano da tabela e vai para a legenda.
- **Motivo:** deflacionamento oficial do produtor, com CV publicado, sem cálculo próprio a validar.
  Decidido pelo mantenedor.
- **Fonte:** https://sidra.ibge.gov.br/tabela/7533

## 2026-10-20 — homicidios: definição, total Brasil e conferência por contagem
- **Decisão:** homicídio = óbitos por agressão (CID-10 X85–Y09) + intervenção legal e operações de
  guerra (Y35–Y36), por UF de residência, do SIM via TabNet. Só anos consolidados (até 2024). O total
  Brasil é o "Total" do TabNet, que inclui residência ignorada/exterior. A conferência com números
  publicados é feita sobre a **contagem de óbitos** (Atlas da Violência). A taxa usa a população única
  da seção 4.2.
- **Motivo:** o total de 2024 do TabNet (42.590) é igual ao do Atlas da Violência 2026, mas as taxas do
  Atlas usam outra população (ex.: AP 45,7 no Atlas, 45,2 com a revisão 2024). Decidido pelo mantenedor.
- **Fonte:** http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sim/cnv/obt10uf.def; Atlas da Violência 2026
  (IPEA/FBSP, 26/05/2026).

## 2026-10-20 — idhm: 2020–2021 no mesmo segmento do Radar, com nota
- **Decisão:** os anos 2020 e 2021 do Radar IDHM ficam no segmento PNADC, com nota explicando que
  foram calculados com a visita 5 da PNADC (nos demais anos, visita 1).
- **Motivo:** o PNUD/FJP publica 2012–2024 como uma série única. Decidido pelo mantenedor.
- **Fonte:** adh_radar_metadados_2012_2024.xlsx (Atlas Brasil).

## 2026-10-21 — renda_pc: segmento PNAD 2001–2015 por microdados, no conceito da PNADC
- **Decisão:** o segmento `pnad` é calculado dos microdados da PNAD anual (2001–2009, 2011–2015), no
  conceito da tabela SIDRA 7533: renda domiciliar (V4614) ÷ moradores sem pensionistas, empregados
  domésticos e seus parentes (V0401 = 1 a 5). A média é **por pessoa** (peso V4729) e **inclui** quem
  mora em domicílio sem rendimento. Universo: domicílios particulares (V0201 = 1 ou 3) com rendimento
  declarado. Para 2001–2012 usamos os pesos **reponderados pela Projeção da População de 2013**, a mesma
  base das PNADs 2013–2015. O CV é estimado por linearização de Taylor com estratos (V4617) e UPAs
  (V4618), sem contribuição de estratos com uma só UPA.
- **Motivo:** a única tabela oficial por UF da PNAD antiga (SIS 2016, Tabela 6.6) usa outro conceito:
  média por domicílio, sem os domicílios sem rendimento. Isso dá ~20% a mais (Brasil 2015: 1.270 contra
  1.057 por pessoa). O conceito da 7533 deixa a sobreposição 2012–2015 comparável. Decidido pelo
  mantenedor (opção A).
- **Conferência (indireta):** o mesmo código calcula também o conceito da SIS. As 308 células da
  Tabela 6.6 (Brasil e UFs, 2004–2015) ficam a até R$ 1,28 do publicado, 307 delas a até R$ 1. Os CVs
  também batem (2015: Brasil 0,99 contra 1,0; RR 10,77 contra 10,8). Dez células vão para
  `referencias.yaml` com `medida: auxiliar` e tolerância de R$ 1, porque a SIS publica valores inteiros.
- **Fonte:** https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_anual/microdados/
  (nota técnica em `reponderacao_2001_2012/nota_tecnica.pdf`); SIS 2016, Tabela 6.6.

## 2026-10-21 — renda_pc: deflator do segmento PNAD
- **Decisão:** valor nominal de setembro do ano (mês de referência da PNAD) × IPCA médio do ano-base ÷
  IPCA de setembro do ano. O ano-base é o último ano da tabela 7533, o mesmo do segmento PNADC. Os
  números-índice vêm da SIDRA 1737, variável 2266. Na conferência com a SIS usamos o INPC
  (SIDRA 1736, variável 2289), de setembro do ano a setembro de 2015, como faz a própria SIS.
- **Motivo:** é o mesmo índice e a mesma base de preços do segmento PNADC (o IBGE deflaciona a 7533
  pelo IPCA). Decidido pelo mantenedor.
- **Fonte:** https://sidra.ibge.gov.br/tabela/1737

## 2026-10-21 — esperanca_vida e mort_infantil: até o último ano com Tábua publicada
- **Decisão:** as duas séries vêm das Projeções da População (Revisão 2024, `e0_T` e `TMI_T`) e vão
  até **2024**, o último ano com Tábua Completa de Mortalidade publicada pelo IBGE. Um ano novo só
  entra quando sair a Tábua dele (a de 2025 sai em novembro de 2026). Os valores são rotulados como
  estimativa do IBGE.
- **Motivo:** até 2024 a série das Projeções coincide com as Tábuas publicadas, inclusive na queda de
  2020–2021 (e0 2021 = 72,8). O valor de 2025 da planilha é projeção feita em 2024, sem dado observado
  por trás, e não tem publicação oficial para conferir. Mais conservador com o princípio 4 do
  PROJECT.md do que "cortar no último ano transcorrido". Decidido pelo mantenedor.
- **Fonte:** https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024

## 2026-10-21 — desocupacao e informalidade: taxa anual oficial do IBGE
- **Decisão:** usar as tabelas anuais da PNAD Contínua no SIDRA — 4562 (desocupação, 2012+) e 4708
  (informalidade, 2016+), com o CV publicado. Não recalcular a média dos trimestres.
- **Motivo:** a seção 4 mandava confirmar se o IBGE publica dado anual oficial; publica, e é o número
  que divulga como "taxa anual" (Brasil 2025: 5,6%; 2024: 6,6%). Ele difere da média simples das taxas
  trimestrais (2024: 6,85%), então recalcular criaria um número que o IBGE não publica.
- **Fonte:** https://sidra.ibge.gov.br/tabela/4562; https://sidra.ibge.gov.br/tabela/4708; release
  IBGE de 20/02/2026 (taxas anuais por UF).

## 2026-10-21 — esgoto: definição, quebra de 2019 e denominador
- **Decisão:** "adequado" = rede geral ou pluvial, ou fossa (séptica) ligada à rede. Na PNADC são dois
  segmentos: 2016–2018 (SIDRA 6735, categoria "Rede geral, rede pluvial ou fossa ligada à rede") e
  2019+ (SIDRA 7192, "Rede geral ou rede pluvial" + "Fossa séptica ligada à rede"), porque o IBGE mudou
  a classificação em 2019. O percentual é o do IBGE, sobre os domicílios **com** banheiro, sanitário ou
  buraco para dejeções; a nota do indicador diz que domicílios sem nenhum deles ficam fora da conta.
- **Motivo:** é a definição do PROJECT.md e a única calculável com as tabelas publicadas para 2016–2018
  (antes de 2019 a "fossa não ligada à rede" mistura fossa séptica e rudimentar). A mudança de
  categorias pede segmentos separados (princípio 2). O denominador do IBGE mantém o número conferível.
  Decidido pelo mantenedor.
- **Fonte:** https://sidra.ibge.gov.br/tabela/6735; https://sidra.ibge.gov.br/tabela/7192

## 2026-10-21 — pobreza e extrema_pobreza: linhas de US$ 6,85 e US$ 2,15 (PPC 2017), SIS 2025
- **Decisão:** usar a série da Síntese de Indicadores Sociais 2025 (Tabela 2.23, PNAD Contínua
  2012–2024), com as linhas de US$ 6,85 e US$ 2,15 PPC 2017, como pede o PROJECT.md. Todos os anos vêm
  da mesma edição. As tabelas ODS do SIDRA (5817, 5877) ficam de fora: usam outras linhas e dão outros
  números (Brasil 2024: 4,7% contra 3,5% da SIS).
- **Motivo:** a dúvida levantada no início (se a SIS já usava as linhas novas do Banco Mundial, PPC
  2021) se resolveu na fonte: a SIS 2025 ainda usa PPC 2017. O IBGE informa que as linhas novas
  entram na próxima edição. **Quando ela sair, a série inteira muda e este indicador deve ser
  refeito com a nova edição**, não emendado.
- **Fonte:** https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2025/Tabelas/xls/2_Distribuicao_Renda_xls.zip;
  notícia IBGE 45344 (03/12/2025).

## 2026-10-21 — pib_pc: PIB real pelo volume encadeado, população única
- **Decisão:** PIB real a preços do último ano das Contas Regionais (hoje 2023) = PIB corrente desse ano
  × série encadeada do volume (tab03) do ano ÷ a do último ano. Sem IPCA. Série de referência 2010,
  2002–2023, sem emenda com as anteriores. O denominador é a população única da seção 4.2.
- **Motivo:** é o método da seção 4.1. Com essa população, o per capita do Brasil em 2023 (R$ 51.693,89)
  coincide com o das Contas Nacionais (SIDRA 6784: R$ 51.693,92). A divulgação das Contas Regionais
  usa a população recenseada e publica per capita de 3% a 8% maiores (Brasil R$ 53.886,67; RR 8,4%
  maior). Decidido pelo mantenedor: manter a população única, com nota.
- **Conferência:** PIB total de 2023 (SP, DF, em R$ milhões), per capita do Brasil nas Contas Nacionais
  e, de forma indireta, o crescimento real acumulado 2002–2023 divulgado pelo IBGE (BR 58,2%; RR
  151,6%; MA 102,8%; SP 52,5%), que confere o encadeamento do volume.
- **Fonte:** https://ftp.ibge.gov.br/Contas_Regionais/2023/xls/Especiais_2002_2023_xls.zip; notícia IBGE
  45142; https://sidra.ibge.gov.br/tabela/6784

## 2026-10-22 — ideb: rede pública no fundamental, rede estadual no ensino médio
- **Decisão:** anos iniciais e finais pela rede pública; ensino médio pela rede estadual, no Brasil e
  nas UFs. Série 2005–2025 (bienal) das planilhas do INEP do Ideb 2025. Anos pares não existem e
  ficam como lacuna; no gráfico, os pontos são ligados só visualmente, por tracejado.
- **Motivo:** o INEP não publica a rede pública do ensino médio por UF (só Total, Estadual e Privada).
  A rede estadual é a que o próprio INEP divulga como "rede pública" do estado no ensino médio
  (Piauí 2025: 4,9 nas duas). Decidido pelo mantenedor.
- **Fonte:** https://download.inep.gov.br/ideb/resultados/divulgacao_regioes_ufs_ideb_2025.zip;
  https://download.inep.gov.br/ideb/resultados/divulgacao_brasil_ideb_2025.zip

## 2026-10-22 — Desempenho do mapa no celular aceito para o MVP
- **Decisão:** manter o MapLibre (seção 5.1) e aceitar, no MVP, o desempenho medido na página do mapa:
  Lighthouse celular 63–64 em desempenho e 100 em acessibilidade (meta da seção 9.5: ≥ 90). As
  páginas de texto atingem 96 / 100.
- **Motivo:** o que falta é o bloqueio da thread principal na inicialização do MapLibre (≈ 1,5 s no
  celular simulado; ≈ 0,5 s sem simulação de CPU, com WebGL por software). Chegar a 90 exigiria trocar
  o mapa (ex.: SVG no nível de UF), revendo a escolha feita pensando na fase municipal. O deslocamento
  de layout já foi zerado (CLS 0). Decidido pelo mantenedor.
- **Revisitar:** com medições em aparelhos reais após o deploy, ou antes da fase municipal.

## 2026-10-22 — Hospedagem: Cloudflare Workers com arquivos estáticos, no lugar do Pages
- **Decisão:** publicar o site como Worker só com arquivos estáticos (`wrangler.jsonc` na raiz,
  pasta `web/dist`), com build ligado ao GitHub (Workers Builds). A seção 5.1 previa Cloudflare Pages.
- **Motivo:** o painel da Cloudflare agora leva projetos novos para Workers, e a própria Cloudflare
  indica Workers com arquivos estáticos como sucessor do Pages; os recursos novos saem lá. Para um
  site estático o resultado é o mesmo: grátis, CDN, `_headers` de cache, prévia por branch e Web
  Analytics sem cookies. O site continua portável (só a pasta `web/dist`). Decidido pelo mantenedor.
