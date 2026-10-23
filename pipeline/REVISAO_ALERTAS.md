# Revisão dos alertas de variação

O validador marca como alerta toda variação de um ano para o outro acima do limite de cada indicador
(ver `pipeline/REPORT.md`). Um alerta não é erro: pede que uma pessoa confira se a variação tem
explicação. Aqui fica o resultado dessa conferência, por indicador e por padrão, com a aprovação do
mantenedor. Ao refazer o build com dados novos, revisar só os alertas que não constam aqui.

## `idhm` — 17 alertas (REPORT de 2026-10-22, limite 8%) — aprovado pelo mantenedor em 2026-10-22

- **Longevidade, 2021→2022 (6 alertas: RO, AC, AM, RR, MT, GO):** recuperação depois das mortes da
  covid-19 em 2020–2021. A mesma queda e volta aparece na esperança de vida do IBGE, que é a base da
  dimensão (AM: 69,7 anos em 2021 e 74,8 em 2022). As quedas de 2020 e 2021 ficaram abaixo do limite.
- **Educação e índice geral, 2020→2021 e 2021→2022 (10 alertas: AC, AM, RR, AP, BA):** queda em 2021
  e volta em 2022. Em 2020 e 2021 o Radar usou a 5ª visita da PNAD Contínua (pandemia); em 2022 voltou
  à 1ª. Os estados são de amostra pequena (RR: 0,753 → 0,670 → 0,813 → 0,782 em 2023).
- **Educação, AP, 2012→2013 (+8,4%):** estado de amostra pequena, sem mudança de método.
- **Conclusão:** valores iguais aos publicados pelo Radar IDHM; nenhum indício de erro de extração.

## `renda_pc` — 50 alertas (REPORT de 2026-10-22, limite 15%) — aprovado pelo mantenedor em 2026-10-22

- **PNAD, 2001–2004 (6 alertas: AC, RR, PA, AP):** até 2003 a PNAD cobria só a área urbana desses
  estados (valores marcados como "cobertura apenas urbana"), com amostra pequena; em 2004 entrou a área
  rural, o que derruba a média (RR 2003→2004: 933,55 → 677,33).
- **PNAD, 2004–2015 (18 alertas: AC, AM, RR, AP, MA, PI, RN, AL, MS, MT):** todos os valores
  2004–2015 do mesmo cálculo, no conceito da SIS 2016 (Tabela 6.6), batem com as 308 células publicadas
  pelo IBGE (diferença de até R$ 1,28; ver DECISIONS.md). Os saltos estão, portanto, também nos números
  do IBGE. Incluem o aumento geral de 2005→2006 no Nordeste (MA +34%, AL +30%) e oscilações de estados
  de amostra pequena (RR, AP, AC). 2009→2011 é um intervalo de dois anos (2010 é ano
  de Censo).
- **PNAD Contínua (26 alertas):** valores iguais aos da tabela SIDRA 7533 (conferidos por amostragem
  em 2026-10-22: DF, RO, AP e Brasil, 2023–2025). Padrões: queda em 2020→2021 (RO, CE, BA) e volta em
  2021→2022 (RO, PA, AP, TO, MA, PI, ES); alta de 2022→2023 em vários estados; oscilações de RR e AP (amostra pequena). O
  maior, DF 2024→2025 (+27,7%: R$ 3.447 → R$ 4.401), é o publicado pelo IBGE (CV 5,9%) e foi noticiado
  com esse número.
- **Conclusão:** nenhum indício de erro de extração ou de cálculo.

## `pib_pc` — 5 alertas (REPORT de 2026-10-22, limite 12%) — aprovado pelo mantenedor em 2026-10-22

- **Todos (AC 2022→2023 +14,2%; TO 2009→2010 +15,6%; ES 2009→2010 +14,0%; MS 2022→2023 +12,5%;
  MT 2003→2004 +12,9%):** a variação real vem da série encadeada do volume do PIB publicada pelo IBGE
  (Contas Regionais, tab03), dividida pela população. O encadeamento confere com o crescimento real
  acumulado 2002–2023 divulgado pelo IBGE (ver DECISIONS.md). 2010 é o ano de recuperação depois da
  queda de 2009 no país.
- **Conclusão:** nenhum indício de erro.

## `gini` — 47 alertas (REPORT de 2026-10-22, limite 8%) — aprovado pelo mantenedor em 2026-10-22

- **PNAD (24 alertas: RO, AC, RR, AP, MA, PI, RN, PB, AL, SE, MT, GO):** o mesmo código, no conceito da
  SIS 2016 (Tabela 6.3, Gini do rendimento das pessoas de 15+ com rendimento), reproduz as 308 células
  publicadas (Brasil e UFs, 2004–2015): 307 iguais e uma com diferença de 0,001 (SP 2005), conferido
  em 2026-10-22. Os alertas são de estados de amostra pequena (AP tem 7; RR, AC e MA, 2 ou 3), de
  2001–2003 (só área urbana no Norte) e de 2009→2011, intervalo de dois anos (2010 é ano de Censo).
  O segmento não tem CV, então essas oscilações não recebem aviso de baixa precisão.
- **PNAD Contínua (23 alertas):** valores iguais aos da tabela SIDRA 7435 (conferidos por amostragem
  em 2026-10-22: PI 2023–2024, BA 2016–2017, RN 2020–2022). Padrão principal: queda em 2019→2020 e
  volta em 2020→2021 (AC, PA, TO, MA, PI, PB, SE e outros) e nova queda em 2021→2022 (RR, RN, PE);
  2020–2022 vêm da 5ª visita. Os demais (RO e PA 2017→2018, BA 2016→2017, PI e PB 2023→2024) são de
  estados com amostra menor.
- **Conclusão:** nenhum indício de erro de extração ou de cálculo.

## `pobreza` — 9 alertas (REPORT de 2026-10-22, limite 25%) — aprovado pelo mantenedor em 2026-10-22

- **Conferência:** os valores dos alertas foram relidos da Tabela 2.23 da SIS 2025 com um script
  independente do pipeline (2026-10-22) e são iguais (ex.: AP 2022→2023: 47,49 → 32,45; SC
  2023→2024: 11,45 → 7,96).
- **Padrões:** alta em 2020→2021 (RO, SE, MG, ES), queda em 2021→2022 ou 2022→2023 (MS, GO, AP, MG) e
  queda em 2023→2024 em SC, onde a proporção é baixa (variações relativas grandes sobre bases
  pequenas). O mesmo desenho aparece no Brasil (31,06 → 36,77 → 31,65 → 27,30 de 2020 a 2023) e
  coincide com os anos em que a SIS usa a 5ª visita (2020–2022).
- **Conclusão:** nenhum indício de erro.

## `extrema_pobreza` — 59 alertas (REPORT de 2026-10-22, limite 35%) — aprovado pelo mantenedor em 2026-10-22

- **Conferência:** relidos da Tabela 2.23 da SIS 2025 com o mesmo script independente (ex.: RN
  2020→2021: 6,38 → 15,13; DF 2016→2017: 1,93 → 3,72; Brasil 2020→2021: 6,05 → 9,02). Iguais.
- **Padrões:** proporções pequenas (muitas abaixo de 5%), em que poucos décimos viram variações
  relativas de 35% a 135%. A maior parte está em 2019→2020 (queda), 2020→2021 (alta) e 2021→2022
  (queda), inclusive no Brasil (+49% em 2020→2021, número divulgado pelo IBGE), e em 2023→2024
  (queda). 48 valores já têm aviso de baixa precisão (CV acima de 15%).
- **Conclusão:** nenhum indício de erro.

## `desocupacao` — 35 alertas (REPORT de 2026-10-22, limite 35%) — aprovado pelo mantenedor em 2026-10-22

- **Conferência:** valores iguais aos da tabela SIDRA 4562 (conferidos em 2026-10-22: RR, MT e RO,
  2014–2016 e 2021–2022; ex.: RR 2021→2022: 13,9 → 4,9).
- **Padrões:** alta de 2014→2015 e 2015→2016 em quase todo o país (20 alertas), queda de 2021→2022
  (10 alertas), alta de 2016→2017 (AC, MS) e de 2019→2020 (PB, AL), e queda de 2022→2023 no AC. Taxas baixas no Sul e no Centro-Oeste fazem variações de
  poucos pontos virarem variações relativas grandes (SC 2014→2015: 3,0 → 4,4).
- **Conclusão:** nenhum indício de erro.

## `informalidade` — 0 alertas (REPORT de 2026-10-22, limite 15%)

- Nada a revisar.

## `ideb` — 55 alertas (REPORT de 2026-10-22, limite 15%) — aprovado pelo mantenedor em 2026-10-22

- **Conferência:** valores conferidos com a planilha do INEP (divulgação Ideb 2025, UFs e regiões),
  incluindo o maior alerta, ensino médio do PA 2021→2023 (3,0 → 4,3; rede estadual), lido em
  2026-10-22 com um script independente do pipeline.
- **Padrões:** o intervalo é de dois anos e a nota tem uma casa decimal, então 0,5 ponto já passa de
  15% em notas baixas. Concentração em 2005→2007 e 2007→2009 (primeiras edições, notas entre 2,3 e
  3,5) e no ensino médio de 2017 em diante.
- **Conclusão:** nenhum indício de erro.

## `analfabetismo` — 32 alertas (REPORT de 2026-10-22, depois do recálculo; limite 20%) — aprovado pelo mantenedor em 2026-10-22

- **Erro encontrado e corrigido:** no REPORT anterior (36 alertas), o DF de 2009 aparecia com 1,45%
  (entre 3,93% e 3,24%) por causa de contagens incompletas na SIDRA 271. O segmento PNAD passou a ser
  calculado dos microdados (DECISIONS.md, 2026-10-22); o DF de 2009 agora é 3,45% e não gera alerta.
  O novo cálculo reproduz as 66 taxas do Brasil e das regiões da SIS 2016 (Tabela 4.15).
- **PNAD, Norte (21 alertas: AC, AM, RR, PA, AP, RO):** amostras pequenas (CVs de 7% a 22%; os acima
  de 15% já têm aviso de baixa precisão) e, em 2003→2004, a entrada da área rural na pesquisa, que
  eleva a taxa (PA: 10,5% → 14,5%; AM: 6,6% → 9,0%).
- **PNAD, 2009→2011 (6 alertas: PB, ES, SP, SC, MS, MT; RR e AP estão no item acima):** intervalo de dois anos (2010 é ano de
  Censo). Nas regiões, as quedas desse intervalo batem com as da SIS 2016.
- **PNAD, 2014→2015 (RS, GO) e DF 2002→2003:** taxas baixas, em que poucos décimos passam de 20%.
- **PNAD Contínua (SC 2024→2025: 1,9 → 1,5; DF 2017→2018: 2,3 → 2,9):** taxas publicadas na SIDRA
  7113, sobre bases muito baixas.
- **Conclusão:** com a correção, nenhum indício de erro.

## `esperanca_vida` — 36 alertas (REPORT de 2026-10-22, limite 3%) — aprovado pelo mantenedor em 2026-10-22

- **Todos em 2019→2022:** queda em 2020 e 2021 e volta em 2022, em quase todos os estados e no Brasil
  (72,78 anos em 2021 e 75,45 em 2022). É o efeito das mortes da covid-19 que o IBGE aponta na
  divulgação das Tábuas. Valores relidos da planilha das Projeções (Revisão 2024, tab4) com um script
  independente em 2026-10-22 (ex.: AC 2021 → 2022: 71,23 → 75,20).
- **Conclusão:** nenhum indício de erro.

## `mort_infantil` — 83 alertas (REPORT de 2026-10-22, limite 15%) — aprovado pelo mantenedor em 2026-10-22

- **Estimativa do IBGE (48 alertas):** valores relidos da planilha das Projeções (Revisão 2024, tab4)
  com um script independente (ex.: RR 2017 → 2018 → 2019: 17,13 → 22,40 → 17,80; AC 2020 → 2021:
  14,89 → 19,44; DF 2018 → 2019 → 2020: 10,43 → 8,21 → 10,09). Iguais. São estados com poucos
  nascimentos (RR, AC, AP, DF) e a queda forte de 2000 a 2010 no Nordeste.
- **Taxa direta do DATASUS (35 alertas, linha de referência):** óbitos de menores de 1 ano ÷
  nascidos vivos, com contagens pequenas nos mesmos estados (RR tem 11 alertas). As contagens vêm do
  mesmo leitor do TabNet usado em homicídios, que reproduz exatamente as contagens do Atlas da
  Violência. Quando a estimativa do IBGE e a taxa direta sobem juntas (RR 2022 → 2023), a variação
  aparece nas duas fontes.
- **Conclusão:** nenhum indício de erro.

## `homicidios` — 15 alertas (REPORT de 2026-10-22, limite 35%) — aprovado pelo mantenedor em 2026-10-22

- **Conferência:** as contagens batem exatamente com o Atlas da Violência 2026 (seis referências,
  incluindo RR 2018 e AP 2023, dois dos estados com alertas).
- **Padrões:** estados de população pequena (AC, RR, AP: poucas dezenas de homicídios a mais mudam
  muito a taxa) e ondas de alta e queda em poucos anos em AC (2016–2017), RR (2012–2013 e 2018–2019),
  CE (2012 e 2017–2020), RJ (2019–2020) e AM (2021), todas também nas contagens do SIM; e MA
  2000→2001, sobre uma taxa baixa (5,96 → 9,41).
- **Conclusão:** nenhum indício de erro.

## `esgoto` — 94 alertas (depois do recálculo; limite 20%) — aprovado pelo mantenedor em 2026-10-22

- **Erro encontrado e corrigido:** no REPORT anterior (125 alertas), a série da PNAD somava só a rede
  coletora de 2001 a 2008 e a rede mais a fossa séptica ligada a partir de 2009, porque a SIDRA 1956
  só separa a fossa ligada desde 2009. Isso subestimava 2001–2008 e criava um salto falso em 2009 (RS:
  16% → 55%; SC: 28% → 57%). O segmento passou a ser calculado dos microdados com a mesma definição em
  todos os anos (DECISIONS.md, 2026-10-22); as 168 contagens de 2009–2015 batem com a SIDRA 1956. Agora
  o Brasil vai de 59,2% (2001) a 66,6% (2015) sem saltos, e o RS fica entre 54% e 59% de 2006 a 2009.
- **PNAD (85 alertas):** quase todos em estados de amostra pequena e com proporções baixas (RO, AC,
  AM, RR, AP, TO, PI, AL, MS, MT), muitos com CV acima de 15% e, portanto, com aviso de baixa
  precisão (107 valores do segmento têm o aviso). Destaques, todos presentes também nas contagens do
  IBGE: AM 2006→2007 (6,4% → 32,5%: a rede coletora passa de 30 mil para 185 mil domicílios na própria
  SIDRA 1956) e as altas de 2009→2011 (intervalo de dois anos) em PB, PE, AL, MA e MS.
- **PNAD Contínua (9 alertas):** RR, PA, AP e PI em 2017→2018 (6735) e RO, AP e PI em 2022–2025
  (7192), valores publicados pelo IBGE; estados pequenos ou com proporções baixas.
- **Conclusão:** com a correção, nenhum indício de erro.

## `inflacao` — 40 alertas (REPORT de 2026-10-23, limite 100%) — aprovado pelo mantenedor em 2026-10-23

- **Conferência:** 12 valores dos alertas relidos da API do SIDRA com um script independente do
  pipeline (2026-10-23), todos iguais (ex.: São Luís 2023→2024, IPCA: 1,70 → 6,51; Curitiba
  2020→2021, IPCA: 3,95 → 12,73; Brasil 2020→2021, IPCA: 4,52 → 10,06; Salvador 2000→2001, INPC:
  4,08 → 11,60; Campo Grande 2017→2018, INPC: 0,85 → 2,57).
- **Padrões:** alta geral de 2020→2021 (15 alertas, inclusive o Brasil); anos seguintes a inflação
  baixa, em que voltar a 3% ou 4% passa do dobro: 2017→2018 e PA 2018→2019 (9), 2006→2007 (7) e São
  Luís 2023→2024 (2); alta de 2001 e 2002 (5); INPC de SP e PR em 2014→2015 (2). O limite é relativo
  e, numa taxa como a inflação, marca sobretudo os anos depois de uma inflação baixa.
- **Conclusão:** nenhum indício de erro de extração.
