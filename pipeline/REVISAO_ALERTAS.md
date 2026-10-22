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

## `analfabetismo` — 32 alertas (REPORT de 2026-10-22, depois do recálculo; limite 20%) — aguardando aprovação

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
