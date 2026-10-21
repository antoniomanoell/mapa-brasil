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
