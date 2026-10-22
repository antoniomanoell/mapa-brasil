# REPORT do pipeline

- Data: 2026-10-22
- Versão do pipeline: `083abb3`
- Escopo: completo
- Resultado: OK

## `idhm` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| geral | Censo (2000, 2010) | 2000, 2010 | 2001–2009 | — |
| geral | Radar IDHM – PNAD Contínua (2012–) | 2012–2024 | — | — |
| longevidade | Censo (2000, 2010) | 2000, 2010 | 2001–2009 | — |
| longevidade | Radar IDHM – PNAD Contínua (2012–) | 2012–2024 | — | — |
| educacao | Censo (2000, 2010) | 2000, 2010 | 2001–2009 | — |
| educacao | Radar IDHM – PNAD Contínua (2012–) | 2012–2024 | — | — |
| renda | Censo (2000, 2010) | 2000, 2010 | 2001–2009 | — |
| renda | Radar IDHM – PNAD Contínua (2012–) | 2012–2024 | — | — |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (17)

- geral/pnadc/13: 2021→2022 variou +8.1% (0.7 → 0.757)
- geral/pnadc/14: 2021→2022 variou +9.9% (0.694 → 0.763)
- geral/pnadc/16: 2021→2022 variou +9.1% (0.681 → 0.743)
- longevidade/pnadc/11: 2021→2022 variou +9.6% (0.759 → 0.832)
- longevidade/pnadc/12: 2021→2022 variou +8.6% (0.771 → 0.837)
- longevidade/pnadc/13: 2021→2022 variou +11.4% (0.745 → 0.83)
- longevidade/pnadc/14: 2021→2022 variou +9.5% (0.735 → 0.805)
- longevidade/pnadc/51: 2021→2022 variou +8.6% (0.766 → 0.832)
- longevidade/pnadc/52: 2021→2022 variou +8.1% (0.778 → 0.841)
- educacao/pnadc/12: 2020→2021 variou -8.4% (0.748 → 0.685)
- educacao/pnadc/13: 2021→2022 variou +8.5% (0.717 → 0.778)
- educacao/pnadc/14: 2020→2021 variou -11.0% (0.753 → 0.67)
- educacao/pnadc/14: 2021→2022 variou +21.3% (0.67 → 0.813)
- educacao/pnadc/16: 2012→2013 variou +8.4% (0.653 → 0.708)
- educacao/pnadc/16: 2020→2021 variou -8.1% (0.7 → 0.643)
- educacao/pnadc/16: 2021→2022 variou +16.6% (0.643 → 0.75)
- educacao/pnadc/29: 2021→2022 variou +9.6% (0.649 → 0.711)

**Conferência com números publicados** (7)

- geral/pnadc/BR/2024 (valor): 0.805 ≈ 0.805 ✓ (https://www.undp.org/pt/brazil/press-releases/brasil-alcanca-pela-primeira-vez-patamar-de-muito-alto-desenvolvimento-humano-aponta-pnud)
- geral/pnadc/BR/2012 (valor): 0.744 ≈ 0.744 ✓ (https://www.undp.org/pt/brazil/news/educacao-longevidade-e-retomada-da-renda-impulsionam-avanco-do-idhm-brasileiro)
- educacao/pnadc/BR/2012 (valor): 0.679 ≈ 0.679 ✓ (https://www.undp.org/pt/brazil/news/educacao-longevidade-e-retomada-da-renda-impulsionam-avanco-do-idhm-brasileiro)
- educacao/pnadc/BR/2024 (valor): 0.798 ≈ 0.798 ✓ (https://www.undp.org/pt/brazil/news/educacao-longevidade-e-retomada-da-renda-impulsionam-avanco-do-idhm-brasileiro)
- longevidade/pnadc/BR/2024 (valor): 0.86 ≈ 0.86 ✓ (https://www.undp.org/pt/brazil/news/educacao-longevidade-e-retomada-da-renda-impulsionam-avanco-do-idhm-brasileiro)
- renda/pnadc/BR/2012 (valor): 0.732 ≈ 0.732 ✓ (https://www.undp.org/pt/brazil/news/educacao-longevidade-e-retomada-da-renda-impulsionam-avanco-do-idhm-brasileiro)
- renda/pnadc/BR/2024 (valor): 0.76 ≈ 0.76 ✓ (https://www.undp.org/pt/brazil/news/educacao-longevidade-e-retomada-da-renda-impulsionam-avanco-do-idhm-brasileiro)

## `renda_pc` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | PNAD (2001–2015) | 2001–2009, 2011–2015 | 2010 | baixa_precisao: 2, cobertura_urbana: 18 |
| principal | PNAD Contínua (2012–) | 2012–2025 | — | — |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (50)

- principal/pnad/12: 2002→2003 variou -15.8% (1236.89 → 1041.75)
- principal/pnad/12: 2003→2004 variou -17.7% (1041.75 → 857.59)
- principal/pnad/12: 2005→2006 variou +19.9% (864.84 → 1037.23)
- principal/pnad/12: 2008→2009 variou +27.0% (1073.16 → 1363.15)
- principal/pnad/13: 2014→2015 variou -16.6% (1362.05 → 1135.4)
- principal/pnad/14: 2003→2004 variou -27.4% (933.55 → 677.33)
- principal/pnad/14: 2004→2005 variou +15.4% (677.33 → 781.42)
- principal/pnad/14: 2005→2006 variou +36.1% (781.42 → 1063.59)
- principal/pnad/14: 2007→2008 variou +22.1% (947.5 → 1156.99)
- principal/pnad/14: 2009→2011 variou +27.7% (1192.78 → 1523.39)
- principal/pnad/15: 2002→2003 variou -15.1% (889.29 → 754.84)
- principal/pnad/16: 2001→2002 variou -16.2% (1088.48 → 912.37)
- principal/pnad/16: 2003→2004 variou -16.0% (970.36 → 815.11)
- principal/pnad/16: 2004→2005 variou +23.5% (815.11 → 1006.52)
- principal/pnad/16: 2011→2012 variou +19.7% (1111.9 → 1330.41)
- principal/pnad/16: 2014→2015 variou -15.2% (1483.12 → 1257.54)
- principal/pnad/21: 2005→2006 variou +34.0% (539.35 → 722.79)
- principal/pnad/22: 2005→2006 variou +17.2% (681.92 → 799.48)
- principal/pnad/22: 2011→2012 variou +25.0% (931.13 → 1164.08)
- principal/pnad/24: 2004→2005 variou +18.0% (772.17 → 911.47)
- principal/pnad/27: 2005→2006 variou +30.3% (599.11 → 780.41)
- principal/pnad/50: 2006→2007 variou +15.9% (1398.82 → 1621.03)
- principal/pnad/50: 2009→2011 variou +17.2% (1619.14 → 1897.34)
- principal/pnad/51: 2007→2008 variou +27.9% (1267.55 → 1621.32)
- principal/pnadc/11: 2020→2021 variou -15.6% (1479.0 → 1249.0)
- principal/pnadc/11: 2021→2022 variou +21.5% (1249.0 → 1517.0)
- principal/pnadc/13: 2022→2023 variou +17.4% (1088.0 → 1277.0)
- principal/pnadc/14: 2017→2018 variou +19.8% (1415.0 → 1695.0)
- principal/pnadc/14: 2018→2019 variou -16.0% (1695.0 → 1424.0)
- principal/pnadc/14: 2024→2025 variou +16.5% (1605.0 → 1870.0)
- principal/pnadc/15: 2017→2018 variou +15.5% (1015.0 → 1172.0)
- principal/pnadc/15: 2021→2022 variou +19.0% (1015.0 → 1208.0)
- principal/pnadc/16: 2021→2022 variou +27.8% (1054.0 → 1347.0)
- principal/pnadc/16: 2022→2023 variou +22.9% (1347.0 → 1655.0)
- principal/pnadc/17: 2021→2022 variou +19.1% (1309.0 → 1559.0)
- principal/pnadc/21: 2021→2022 variou +18.7% (790.0 → 938.0)
- principal/pnadc/22: 2012→2013 variou +20.7% (975.0 → 1177.0)
- principal/pnadc/22: 2021→2022 variou +17.1% (1060.0 → 1241.0)
- principal/pnadc/22: 2022→2023 variou +15.9% (1241.0 → 1438.0)
- principal/pnadc/23: 2020→2021 variou -15.7% (1326.0 → 1118.0)
- principal/pnadc/25: 2022→2023 variou +18.0% (1236.0 → 1458.0)
- principal/pnadc/26: 2023→2024 variou +23.8% (1187.0 → 1470.0)
- principal/pnadc/28: 2023→2024 variou +15.5% (1294.0 → 1494.0)
- principal/pnadc/29: 2020→2021 variou -16.9% (1261.0 → 1048.0)
- principal/pnadc/29: 2023→2024 variou +15.2% (1209.0 → 1393.0)
- principal/pnadc/31: 2022→2023 variou +18.9% (1736.0 → 2064.0)
- principal/pnadc/32: 2021→2022 variou +18.5% (1596.0 → 1892.0)
- principal/pnadc/51: 2022→2023 variou +15.5% (1855.0 → 2143.0)
- principal/pnadc/52: 2022→2023 variou +20.3% (1782.0 → 2143.0)
- principal/pnadc/53: 2024→2025 variou +27.7% (3447.0 → 4401.0)

**Conferência com números publicados** (13)

- principal/pnadc/BR/2025 (valor): 2264.0 ≈ 2264 ✓ (https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf)
- principal/pnadc/BR/2024 (valor): 2118.0 ≈ 2118 ✓ (https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf)
- principal/pnadc/BR/2019 (valor): 1904.0 ≈ 1904 ✓ (https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf)
- principal/pnad/BR/2015 (auxiliar sis2016_tab6_6): 1270.23 ≈ 1270 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/BR/2004 (auxiliar sis2016_tab6_6): 909.94 ≈ 910 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/BR/2009 (auxiliar sis2016_tab6_6): 1139.25 ≈ 1139 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/11/2015 (auxiliar sis2016_tab6_6): 1061.37 ≈ 1061 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/26/2008 (auxiliar sis2016_tab6_6): 718.63 ≈ 718 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/35/2012 (auxiliar sis2016_tab6_6): 1689.31 ≈ 1689 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/53/2004 (auxiliar sis2016_tab6_6): 1789.07 ≈ 1789 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/43/2006 (auxiliar sis2016_tab6_6): 1228.31 ≈ 1228 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/21/2011 (auxiliar sis2016_tab6_6): 624.46 ≈ 624 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/14/2013 (auxiliar sis2016_tab6_6): 1121.44 ≈ 1121 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)

## `pib_pc` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | Contas Regionais, ref. 2010 (2002–2023) | 2002–2023 | — | — |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (5)

- principal/cr2010/12: 2022→2023 variou +14.2% (26261.97 → 29993.0)
- principal/cr2010/17: 2009→2010 variou +15.6% (24999.25 → 28902.16)
- principal/cr2010/32: 2009→2010 variou +14.0% (48279.19 → 55043.39)
- principal/cr2010/50: 2022→2023 variou +12.5% (56947.94 → 64072.81)
- principal/cr2010/51: 2003→2004 variou +12.9% (35887.94 → 40503.6)

**Conferência com números publicados** (7)

- principal/cr2010/35/2023 (contagem): 3444814.0 ≈ 3444814 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45142-pib-cresce-em-todos-os-27-estados-do-pais-em-2023)
- principal/cr2010/53/2023 (contagem): 365669.1 ≈ 365669 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45142-pib-cresce-em-todos-os-27-estados-do-pais-em-2023)
- principal/cr2010/BR/2023 (auxiliar cr_volume_acumulado): 58.2 ≈ 58.2 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45142-pib-cresce-em-todos-os-27-estados-do-pais-em-2023)
- principal/cr2010/14/2023 (auxiliar cr_volume_acumulado): 151.63 ≈ 151.6 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45142-pib-cresce-em-todos-os-27-estados-do-pais-em-2023)
- principal/cr2010/21/2023 (auxiliar cr_volume_acumulado): 102.78 ≈ 102.8 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45142-pib-cresce-em-todos-os-27-estados-do-pais-em-2023)
- principal/cr2010/35/2023 (auxiliar cr_volume_acumulado): 52.55 ≈ 52.5 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45142-pib-cresce-em-todos-os-27-estados-do-pais-em-2023)
- principal/cr2010/BR/2023 (valor): 51693.89 ≈ 51693.92 ✓ (https://sidra.ibge.gov.br/tabela/6784)

## `gini` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | PNAD (2001–2015) | 2001–2009, 2011–2015 | 2010 | cobertura_urbana: 18 |
| principal | PNAD Contínua (2012–) | 2012–2025 | — | — |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (47)

- principal/pnad/11: 2004→2005 variou +10.3% (0.515 → 0.568)
- principal/pnad/12: 2007→2008 variou -8.2% (0.61 → 0.56)
- principal/pnad/12: 2008→2009 variou +9.5% (0.56 → 0.613)
- principal/pnad/12: 2009→2011 variou -11.1% (0.613 → 0.545)
- principal/pnad/14: 2003→2004 variou +11.0% (0.525 → 0.583)
- principal/pnad/14: 2006→2007 variou -8.7% (0.565 → 0.516)
- principal/pnad/16: 2001→2002 variou +14.6% (0.481 → 0.551)
- principal/pnad/16: 2002→2003 variou +8.5% (0.551 → 0.598)
- principal/pnad/16: 2003→2004 variou -9.4% (0.598 → 0.542)
- principal/pnad/16: 2005→2006 variou -9.3% (0.527 → 0.478)
- principal/pnad/16: 2007→2008 variou -10.8% (0.509 → 0.454)
- principal/pnad/16: 2008→2009 variou +14.3% (0.454 → 0.519)
- principal/pnad/16: 2013→2014 variou -10.0% (0.522 → 0.47)
- principal/pnad/21: 2004→2005 variou -14.8% (0.609 → 0.519)
- principal/pnad/21: 2005→2006 variou +14.8% (0.519 → 0.596)
- principal/pnad/22: 2009→2011 variou -8.5% (0.554 → 0.507)
- principal/pnad/24: 2013→2014 variou -8.2% (0.538 → 0.494)
- principal/pnad/25: 2009→2011 variou -8.8% (0.588 → 0.536)
- principal/pnad/27: 2005→2006 variou +10.6% (0.564 → 0.624)
- principal/pnad/27: 2009→2011 variou -8.3% (0.569 → 0.522)
- principal/pnad/28: 2013→2014 variou -13.1% (0.556 → 0.483)
- principal/pnad/51: 2011→2012 variou +9.0% (0.476 → 0.519)
- principal/pnad/51: 2013→2014 variou -8.8% (0.501 → 0.457)
- principal/pnad/52: 2005→2006 variou -8.3% (0.552 → 0.506)
- principal/pnadc/11: 2017→2018 variou +11.2% (0.447 → 0.497)
- principal/pnadc/12: 2019→2020 variou -8.0% (0.56 → 0.515)
- principal/pnadc/14: 2020→2021 variou +10.6% (0.54 → 0.597)
- principal/pnadc/14: 2021→2022 variou -8.2% (0.597 → 0.548)
- principal/pnadc/15: 2017→2018 variou +10.9% (0.506 → 0.561)
- principal/pnadc/15: 2019→2020 variou -9.3% (0.528 → 0.479)
- principal/pnadc/15: 2020→2021 variou +10.2% (0.479 → 0.528)
- principal/pnadc/17: 2019→2020 variou -8.5% (0.531 → 0.486)
- principal/pnadc/21: 2019→2020 variou -9.2% (0.531 → 0.482)
- principal/pnadc/21: 2020→2021 variou +9.8% (0.482 → 0.529)
- principal/pnadc/22: 2019→2020 variou -11.9% (0.538 → 0.474)
- principal/pnadc/22: 2020→2021 variou +8.6% (0.474 → 0.515)
- principal/pnadc/22: 2023→2024 variou -10.2% (0.549 → 0.493)
- principal/pnadc/24: 2020→2021 variou +14.6% (0.513 → 0.588)
- principal/pnadc/24: 2021→2022 variou -11.1% (0.588 → 0.523)
- principal/pnadc/25: 2019→2020 variou -8.5% (0.563 → 0.515)
- principal/pnadc/25: 2020→2021 variou +9.1% (0.515 → 0.562)
- principal/pnadc/25: 2023→2024 variou -11.6% (0.561 → 0.496)
- principal/pnadc/26: 2020→2021 variou +8.2% (0.536 → 0.58)
- principal/pnadc/26: 2021→2022 variou -11.4% (0.58 → 0.514)
- principal/pnadc/28: 2019→2020 variou -10.0% (0.58 → 0.522)
- principal/pnadc/28: 2020→2021 variou +8.4% (0.522 → 0.566)
- principal/pnadc/29: 2016→2017 variou +9.1% (0.537 → 0.586)

**Conferência com números publicados** (8)

- principal/pnadc/BR/2025 (valor): 0.511 ≈ 0.511 ✓ (https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf)
- principal/pnadc/BR/2024 (valor): 0.504 ≈ 0.504 ✓ (https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf)
- principal/pnadc/BR/2019 (valor): 0.543 ≈ 0.543 ✓ (https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf)
- principal/pnad/BR/2015 (auxiliar sis2016_tab6_3): 0.491 ≈ 0.491 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/35/2015 (auxiliar sis2016_tab6_3): 0.46 ≈ 0.46 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/42/2015 (auxiliar sis2016_tab6_3): 0.419 ≈ 0.419 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/25/2015 (auxiliar sis2016_tab6_3): 0.51 ≈ 0.51 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)
- principal/pnad/27/2015 (auxiliar sis2016_tab6_3): 0.438 ≈ 0.438 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip)

## `pobreza` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | SIS 2025 – PNAD Contínua (2012–2024) | 2012–2024 | — | — |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (9)

- principal/sis_pnadc/11: 2020→2021 variou +36.5% (28.81 → 39.32)
- principal/sis_pnadc/16: 2022→2023 variou -31.7% (47.49 → 32.45)
- principal/sis_pnadc/28: 2020→2021 variou +26.6% (44.21 → 55.99)
- principal/sis_pnadc/31: 2020→2021 variou +28.7% (24.46 → 31.49)
- principal/sis_pnadc/31: 2022→2023 variou -27.5% (27.07 → 19.63)
- principal/sis_pnadc/32: 2020→2021 variou +29.9% (26.41 → 34.31)
- principal/sis_pnadc/42: 2023→2024 variou -30.5% (11.45 → 7.96)
- principal/sis_pnadc/50: 2021→2022 variou -28.7% (29.83 → 21.27)
- principal/sis_pnadc/52: 2021→2022 variou -27.6% (31.7 → 22.95)

**Conferência com números publicados** (3)

- principal/sis_pnadc/BR/2024 (valor): 23.11 ≈ 23.1 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45344-8-6-milhoes-de-pessoas-sairam-da-pobreza-entre-2023-e-2024)
- principal/sis_pnadc/BR/2023 (valor): 27.3 ≈ 27.3 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45344-8-6-milhoes-de-pessoas-sairam-da-pobreza-entre-2023-e-2024)
- principal/sis_pnadc/BR/2012 (valor): 34.73 ≈ 34.7 ✓ (https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/71016b2eb0a5feb8f7685271b1233db7.pdf)

## `extrema_pobreza` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | SIS 2025 – PNAD Contínua (2012–2024) | 2012–2024 | — | baixa_precisao: 48 |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (59)

- principal/sis_pnadc/11: 2020→2021 variou +55.0% (5.27 → 8.17)
- principal/sis_pnadc/11: 2021→2022 variou -47.6% (8.17 → 4.28)
- principal/sis_pnadc/11: 2023→2024 variou -61.5% (4.31 → 1.66)
- principal/sis_pnadc/12: 2015→2016 variou +36.1% (11.87 → 16.15)
- principal/sis_pnadc/12: 2019→2020 variou -41.2% (18.11 → 10.64)
- principal/sis_pnadc/12: 2020→2021 variou +67.4% (10.64 → 17.81)
- principal/sis_pnadc/12: 2023→2024 variou -43.2% (13.36 → 7.59)
- principal/sis_pnadc/13: 2021→2022 variou -35.6% (16.28 → 10.49)
- principal/sis_pnadc/13: 2022→2023 variou -36.9% (10.49 → 6.62)
- principal/sis_pnadc/15: 2019→2020 variou -39.7% (13.88 → 8.37)
- principal/sis_pnadc/15: 2020→2021 variou +84.6% (8.37 → 15.45)
- principal/sis_pnadc/15: 2021→2022 variou -50.8% (15.45 → 7.6)
- principal/sis_pnadc/16: 2014→2015 variou +59.4% (7.12 → 11.35)
- principal/sis_pnadc/16: 2022→2023 variou -55.0% (7.8 → 3.51)
- principal/sis_pnadc/17: 2017→2018 variou +39.7% (5.79 → 8.09)
- principal/sis_pnadc/21: 2020→2021 variou +49.8% (15.03 → 22.52)
- principal/sis_pnadc/22: 2019→2020 variou -37.5% (15.89 → 9.93)
- principal/sis_pnadc/22: 2020→2021 variou +61.6% (9.93 → 16.05)
- principal/sis_pnadc/22: 2023→2024 variou -50.4% (8.03 → 3.98)
- principal/sis_pnadc/23: 2020→2021 variou +63.1% (9.96 → 16.24)
- principal/sis_pnadc/24: 2019→2020 variou -47.6% (12.18 → 6.38)
- principal/sis_pnadc/24: 2020→2021 variou +137.1% (6.38 → 15.13)
- principal/sis_pnadc/24: 2021→2022 variou -37.1% (15.13 → 9.51)
- principal/sis_pnadc/25: 2020→2021 variou +70.3% (9.78 → 16.66)
- principal/sis_pnadc/25: 2023→2024 variou -35.2% (7.33 → 4.75)
- principal/sis_pnadc/26: 2020→2021 variou +56.3% (12.52 → 19.57)
- principal/sis_pnadc/26: 2021→2022 variou -39.9% (19.57 → 11.76)
- principal/sis_pnadc/28: 2015→2016 variou +37.9% (9.03 → 12.45)
- principal/sis_pnadc/28: 2019→2020 variou -40.0% (14.16 → 8.5)
- principal/sis_pnadc/28: 2020→2021 variou +76.2% (8.5 → 14.98)
- principal/sis_pnadc/28: 2021→2022 variou -40.4% (14.98 → 8.93)
- principal/sis_pnadc/28: 2023→2024 variou -44.8% (8.12 → 4.48)
- principal/sis_pnadc/29: 2020→2021 variou +65.5% (10.39 → 17.2)
- principal/sis_pnadc/29: 2023→2024 variou -35.8% (8.89 → 5.71)
- principal/sis_pnadc/31: 2015→2016 variou +53.8% (3.14 → 4.83)
- principal/sis_pnadc/31: 2020→2021 variou +55.4% (3.41 → 5.3)
- principal/sis_pnadc/31: 2021→2022 variou -40.0% (5.3 → 3.18)
- principal/sis_pnadc/32: 2020→2021 variou +61.9% (4.46 → 7.22)
- principal/sis_pnadc/32: 2021→2022 variou -43.2% (7.22 → 4.1)
- principal/sis_pnadc/32: 2023→2024 variou -35.2% (2.67 → 1.73)
- principal/sis_pnadc/33: 2021→2022 variou -40.2% (7.58 → 4.53)
- principal/sis_pnadc/35: 2021→2022 variou -35.7% (4.45 → 2.86)
- principal/sis_pnadc/41: 2019→2020 variou +37.4% (2.86 → 3.93)
- principal/sis_pnadc/42: 2015→2016 variou +71.3% (1.08 → 1.85)
- principal/sis_pnadc/43: 2022→2023 variou -48.4% (2.48 → 1.28)
- principal/sis_pnadc/50: 2013→2014 variou -39.7% (2.32 → 1.4)
- principal/sis_pnadc/50: 2014→2015 variou +67.1% (1.4 → 2.34)
- principal/sis_pnadc/50: 2016→2017 variou +75.4% (1.91 → 3.35)
- principal/sis_pnadc/50: 2020→2021 variou +49.4% (2.65 → 3.96)
- principal/sis_pnadc/51: 2022→2023 variou -36.4% (4.07 → 2.59)
- principal/sis_pnadc/51: 2023→2024 variou -36.7% (2.59 → 1.64)
- principal/sis_pnadc/52: 2015→2016 variou +77.1% (2.1 → 3.72)
- principal/sis_pnadc/52: 2022→2023 variou -51.3% (2.71 → 1.32)
- principal/sis_pnadc/53: 2016→2017 variou +92.7% (1.93 → 3.72)
- principal/sis_pnadc/53: 2018→2019 variou -46.3% (3.37 → 1.81)
- principal/sis_pnadc/53: 2019→2020 variou +59.7% (1.81 → 2.89)
- principal/sis_pnadc/53: 2020→2021 variou +50.9% (2.89 → 4.36)
- principal/sis_pnadc/53: 2021→2022 variou -59.9% (4.36 → 1.75)
- principal/sis_pnadc/BR: 2020→2021 variou +49.1% (6.05 → 9.02)

**Conferência com números publicados** (3)

- principal/sis_pnadc/BR/2024 (valor): 3.47 ≈ 3.5 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45344-8-6-milhoes-de-pessoas-sairam-da-pobreza-entre-2023-e-2024)
- principal/sis_pnadc/BR/2023 (valor): 4.4 ≈ 4.4 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45344-8-6-milhoes-de-pessoas-sairam-da-pobreza-entre-2023-e-2024)
- principal/sis_pnadc/BR/2012 (valor): 6.59 ≈ 6.6 ✓ (https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/71016b2eb0a5feb8f7685271b1233db7.pdf)

## `desocupacao` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | PNAD Contínua (2012–) | 2012–2025 | — | baixa_precisao: 2 |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (35)

- principal/pnadc/11: 2014→2015 variou +46.2% (3.9 → 5.7)
- principal/pnadc/11: 2015→2016 variou +42.1% (5.7 → 8.1)
- principal/pnadc/11: 2021→2022 variou -55.3% (9.4 → 4.2)
- principal/pnadc/12: 2016→2017 variou +36.5% (10.4 → 14.2)
- principal/pnadc/12: 2022→2023 variou -39.3% (12.2 → 7.4)
- principal/pnadc/13: 2015→2016 variou +48.9% (9.4 → 14.0)
- principal/pnadc/14: 2021→2022 variou -64.7% (13.9 → 4.9)
- principal/pnadc/16: 2015→2016 variou +46.8% (10.9 → 16.0)
- principal/pnadc/17: 2014→2015 variou +47.0% (6.6 → 9.7)
- principal/pnadc/17: 2021→2022 variou -45.8% (14.2 → 7.7)
- principal/pnadc/21: 2021→2022 variou -35.4% (17.8 → 11.5)
- principal/pnadc/22: 2014→2015 variou +36.7% (6.0 → 8.2)
- principal/pnadc/23: 2015→2016 variou +35.2% (8.8 → 11.9)
- principal/pnadc/25: 2019→2020 variou +41.3% (12.6 → 17.8)
- principal/pnadc/26: 2015→2016 variou +46.6% (10.3 → 15.1)
- principal/pnadc/27: 2019→2020 variou +35.4% (14.4 → 19.5)
- principal/pnadc/27: 2021→2022 variou -36.2% (18.8 → 12.0)
- principal/pnadc/28: 2021→2022 variou -36.2% (20.7 → 13.2)
- principal/pnadc/29: 2015→2016 variou +43.4% (11.3 → 16.2)
- principal/pnadc/31: 2021→2022 variou -36.9% (12.2 → 7.7)
- principal/pnadc/32: 2015→2016 variou +37.8% (9.0 → 12.4)
- principal/pnadc/33: 2015→2016 variou +43.0% (8.6 → 12.3)
- principal/pnadc/35: 2014→2015 variou +36.5% (7.4 → 10.1)
- principal/pnadc/35: 2021→2022 variou -36.8% (14.4 → 9.1)
- principal/pnadc/41: 2014→2015 variou +53.8% (3.9 → 6.0)
- principal/pnadc/41: 2015→2016 variou +36.7% (6.0 → 8.2)
- principal/pnadc/42: 2014→2015 variou +46.7% (3.0 → 4.4)
- principal/pnadc/42: 2015→2016 variou +47.7% (4.4 → 6.5)
- principal/pnadc/50: 2014→2015 variou +61.0% (4.1 → 6.6)
- principal/pnadc/50: 2016→2017 variou +37.1% (7.0 → 9.6)
- principal/pnadc/50: 2021→2022 variou -47.4% (9.5 → 5.0)
- principal/pnadc/51: 2014→2015 variou +47.6% (4.2 → 6.2)
- principal/pnadc/51: 2015→2016 variou +54.8% (6.2 → 9.6)
- principal/pnadc/51: 2021→2022 variou -57.4% (9.4 → 4.0)
- principal/pnadc/52: 2015→2016 variou +42.7% (7.5 → 10.7)

**Conferência com números publicados** (5)

- principal/pnadc/BR/2025 (valor): 5.6 ≈ 5.6 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45920-pnad-continua-taxas-anuais-de-desocupacao-sao-as-menores-da-serie-em-20-unidades-da-federacao)
- principal/pnadc/BR/2024 (valor): 6.6 ≈ 6.6 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45920-pnad-continua-taxas-anuais-de-desocupacao-sao-as-menores-da-serie-em-20-unidades-da-federacao)
- principal/pnadc/22/2025 (valor): 9.3 ≈ 9.3 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45920-pnad-continua-taxas-anuais-de-desocupacao-sao-as-menores-da-serie-em-20-unidades-da-federacao)
- principal/pnadc/51/2025 (valor): 2.2 ≈ 2.2 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45920-pnad-continua-taxas-anuais-de-desocupacao-sao-as-menores-da-serie-em-20-unidades-da-federacao)
- principal/pnadc/16/2025 (valor): 7.9 ≈ 7.9 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45920-pnad-continua-taxas-anuais-de-desocupacao-sao-as-menores-da-serie-em-20-unidades-da-federacao)

## `informalidade` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | PNAD Contínua (2016–) | 2016–2025 | — | — |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (0)

- nenhum

**Conferência com números publicados** (4)

- principal/pnadc/BR/2025 (valor): 38.1 ≈ 38.1 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45920-pnad-continua-taxas-anuais-de-desocupacao-sao-as-menores-da-serie-em-20-unidades-da-federacao)
- principal/pnadc/21/2025 (valor): 58.7 ≈ 58.7 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45920-pnad-continua-taxas-anuais-de-desocupacao-sao-as-menores-da-serie-em-20-unidades-da-federacao)
- principal/pnadc/42/2025 (valor): 26.3 ≈ 26.3 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45920-pnad-continua-taxas-anuais-de-desocupacao-sao-as-menores-da-serie-em-20-unidades-da-federacao)
- principal/pnadc/53/2025 (valor): 27.3 ≈ 27.3 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45920-pnad-continua-taxas-anuais-de-desocupacao-sao-as-menores-da-serie-em-20-unidades-da-federacao)

## `analfabetismo` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | PNAD (2001–2015) | 2001–2009, 2011–2015 | 2010 | baixa_precisao: 11, cobertura_urbana: 18 |
| principal | PNAD Contínua (2016–) | 2016–2025 | — | — |

**Lacunas pontuais**

- principal/pnadc/11/2020: valor não publicado pelo IBGE
- principal/pnadc/11/2021: valor não publicado pelo IBGE
- principal/pnadc/12/2020: valor não publicado pelo IBGE
- principal/pnadc/12/2021: valor não publicado pelo IBGE
- principal/pnadc/13/2020: valor não publicado pelo IBGE
- principal/pnadc/13/2021: valor não publicado pelo IBGE
- principal/pnadc/14/2020: valor não publicado pelo IBGE
- principal/pnadc/14/2021: valor não publicado pelo IBGE
- principal/pnadc/15/2020: valor não publicado pelo IBGE
- principal/pnadc/15/2021: valor não publicado pelo IBGE
- principal/pnadc/16/2020: valor não publicado pelo IBGE
- principal/pnadc/16/2021: valor não publicado pelo IBGE
- principal/pnadc/17/2020: valor não publicado pelo IBGE
- principal/pnadc/17/2021: valor não publicado pelo IBGE
- principal/pnadc/21/2020: valor não publicado pelo IBGE
- principal/pnadc/21/2021: valor não publicado pelo IBGE
- principal/pnadc/22/2020: valor não publicado pelo IBGE
- principal/pnadc/22/2021: valor não publicado pelo IBGE
- principal/pnadc/23/2020: valor não publicado pelo IBGE
- principal/pnadc/23/2021: valor não publicado pelo IBGE
- principal/pnadc/24/2020: valor não publicado pelo IBGE
- principal/pnadc/24/2021: valor não publicado pelo IBGE
- principal/pnadc/25/2020: valor não publicado pelo IBGE
- principal/pnadc/25/2021: valor não publicado pelo IBGE
- principal/pnadc/26/2020: valor não publicado pelo IBGE
- principal/pnadc/26/2021: valor não publicado pelo IBGE
- principal/pnadc/27/2020: valor não publicado pelo IBGE
- principal/pnadc/27/2021: valor não publicado pelo IBGE
- principal/pnadc/28/2020: valor não publicado pelo IBGE
- principal/pnadc/28/2021: valor não publicado pelo IBGE
- principal/pnadc/29/2020: valor não publicado pelo IBGE
- principal/pnadc/29/2021: valor não publicado pelo IBGE
- principal/pnadc/31/2020: valor não publicado pelo IBGE
- principal/pnadc/31/2021: valor não publicado pelo IBGE
- principal/pnadc/32/2020: valor não publicado pelo IBGE
- principal/pnadc/32/2021: valor não publicado pelo IBGE
- principal/pnadc/33/2020: valor não publicado pelo IBGE
- principal/pnadc/33/2021: valor não publicado pelo IBGE
- principal/pnadc/35/2020: valor não publicado pelo IBGE
- principal/pnadc/35/2021: valor não publicado pelo IBGE
- principal/pnadc/41/2020: valor não publicado pelo IBGE
- principal/pnadc/41/2021: valor não publicado pelo IBGE
- principal/pnadc/42/2020: valor não publicado pelo IBGE
- principal/pnadc/42/2021: valor não publicado pelo IBGE
- principal/pnadc/43/2020: valor não publicado pelo IBGE
- principal/pnadc/43/2021: valor não publicado pelo IBGE
- principal/pnadc/50/2020: valor não publicado pelo IBGE
- principal/pnadc/50/2021: valor não publicado pelo IBGE
- principal/pnadc/51/2020: valor não publicado pelo IBGE
- principal/pnadc/51/2021: valor não publicado pelo IBGE
- principal/pnadc/52/2020: valor não publicado pelo IBGE
- principal/pnadc/52/2021: valor não publicado pelo IBGE
- principal/pnadc/53/2020: valor não publicado pelo IBGE
- principal/pnadc/53/2021: valor não publicado pelo IBGE
- principal/pnadc/BR/2020: valor não publicado pelo IBGE
- principal/pnadc/BR/2021: valor não publicado pelo IBGE

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (32)

- principal/pnad/11: 2003→2004 variou +22.6% (8.58 → 10.52)
- principal/pnad/12: 2001→2002 variou -22.4% (16.73 → 12.98)
- principal/pnad/12: 2002→2003 variou +29.9% (12.98 → 16.86)
- principal/pnad/13: 2003→2004 variou +36.0% (6.61 → 8.99)
- principal/pnad/13: 2004→2005 variou -25.6% (8.99 → 6.69)
- principal/pnad/14: 2002→2003 variou -20.3% (12.13 → 9.67)
- principal/pnad/14: 2005→2006 variou -29.4% (12.48 → 8.81)
- principal/pnad/14: 2006→2007 variou +24.9% (8.81 → 11.0)
- principal/pnad/14: 2009→2011 variou +24.0% (7.76 → 9.62)
- principal/pnad/14: 2011→2012 variou -23.2% (9.62 → 7.39)
- principal/pnad/14: 2012→2013 variou +32.7% (7.39 → 9.81)
- principal/pnad/14: 2013→2014 variou -23.9% (9.81 → 7.47)
- principal/pnad/15: 2003→2004 variou +38.3% (10.5 → 14.52)
- principal/pnad/16: 2002→2003 variou +49.0% (6.21 → 9.25)
- principal/pnad/16: 2005→2006 variou -28.1% (7.43 → 5.34)
- principal/pnad/16: 2006→2007 variou +34.3% (5.34 → 7.17)
- principal/pnad/16: 2007→2008 variou -34.9% (7.17 → 4.67)
- principal/pnad/16: 2008→2009 variou -30.2% (4.67 → 3.26)
- principal/pnad/16: 2009→2011 variou +133.1% (3.26 → 7.6)
- principal/pnad/16: 2013→2014 variou -29.3% (5.97 → 4.22)
- principal/pnad/16: 2014→2015 variou +39.6% (4.22 → 5.89)
- principal/pnad/25: 2009→2011 variou -20.3% (21.62 → 17.23)
- principal/pnad/32: 2009→2011 variou -25.2% (8.53 → 6.38)
- principal/pnad/35: 2009→2011 variou -22.7% (4.75 → 3.67)
- principal/pnad/42: 2009→2011 variou -21.0% (4.91 → 3.88)
- principal/pnad/43: 2014→2015 variou -21.0% (4.47 → 3.53)
- principal/pnad/50: 2009→2011 variou -26.8% (8.7 → 6.37)
- principal/pnad/51: 2009→2011 variou -27.2% (10.15 → 7.39)
- principal/pnad/52: 2014→2015 variou -20.7% (7.68 → 6.09)
- principal/pnad/53: 2002→2003 variou -21.0% (5.67 → 4.48)
- principal/pnadc/42: 2024→2025 variou -21.1% (1.9 → 1.5)
- principal/pnadc/53: 2017→2018 variou +26.1% (2.3 → 2.9)

**Conferência com números publicados** (6)

- principal/pnadc/BR/2025 (valor): 4.9 ≈ 4.9 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/47221-analfabetismo-fica-abaixo-de-5-em-2025-mas-8-4-milhoes-ainda-nao-sabem-ler-e-escrever)
- principal/pnadc/BR/2024 (valor): 5.3 ≈ 5.3 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/43699-indicadores-educacionais-avancam-em-2024-mas-atraso-escolar-aumenta)
- principal/pnad/BR/2015 (valor): 7.95 ≈ 8.0 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/4_educacao_xls.zip)
- principal/pnad/BR/2004 (valor): 11.45 ≈ 11.5 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/4_educacao_xls.zip)
- principal/pnad/BR/2009 (valor): 9.7 ≈ 9.7 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/4_educacao_xls.zip)
- principal/pnad/BR/2011 (valor): 8.58 ≈ 8.6 ✓ (https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/4_educacao_xls.zip)

## `ideb` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| anos_iniciais | INEP (2005–2025, bienal) | 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023, 2025 | 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024 | — |
| anos_finais | INEP (2005–2025, bienal) | 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023, 2025 | 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024 | — |
| medio | INEP (2005–2025, bienal) | 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023, 2025 | 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024 | — |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (55)

- anos_iniciais/inep/13: 2005→2007 variou +17.2% (2.9 → 3.4)
- anos_iniciais/inep/15: 2007→2009 variou +20.0% (3.0 → 3.6)
- anos_iniciais/inep/16: 2007→2009 variou +15.2% (3.3 → 3.8)
- anos_iniciais/inep/17: 2005→2007 variou +17.6% (3.4 → 4.0)
- anos_iniciais/inep/21: 2005→2007 variou +29.6% (2.7 → 3.5)
- anos_iniciais/inep/21: 2013→2015 variou +15.8% (3.8 → 4.4)
- anos_iniciais/inep/22: 2005→2007 variou +26.9% (2.6 → 3.3)
- anos_iniciais/inep/22: 2007→2009 variou +15.2% (3.3 → 3.8)
- anos_iniciais/inep/23: 2005→2007 variou +25.0% (2.8 → 3.5)
- anos_iniciais/inep/23: 2007→2009 variou +17.1% (3.5 → 4.1)
- anos_iniciais/inep/24: 2005→2007 variou +28.0% (2.5 → 3.2)
- anos_iniciais/inep/25: 2005→2007 variou +22.2% (2.7 → 3.3)
- anos_iniciais/inep/26: 2005→2007 variou +17.9% (2.8 → 3.3)
- anos_iniciais/inep/27: 2005→2007 variou +29.2% (2.4 → 3.1)
- anos_iniciais/inep/27: 2013→2015 variou +16.2% (3.7 → 4.3)
- anos_iniciais/inep/29: 2005→2007 variou +28.0% (2.5 → 3.2)
- anos_iniciais/inep/31: 2007→2009 variou +19.6% (4.6 → 5.5)
- anos_iniciais/inep/50: 2005→2007 variou +20.6% (3.4 → 4.1)
- anos_iniciais/inep/51: 2005→2007 variou +22.9% (3.5 → 4.3)
- anos_finais/inep/11: 2015→2017 variou +17.1% (4.1 → 4.8)
- anos_finais/inep/13: 2005→2007 variou +23.1% (2.6 → 3.2)
- anos_finais/inep/23: 2005→2007 variou +17.9% (2.8 → 3.3)
- anos_finais/inep/25: 2019→2021 variou +15.4% (3.9 → 4.5)
- anos_finais/inep/26: 2007→2009 variou +15.4% (2.6 → 3.0)
- anos_finais/inep/27: 2015→2017 variou +21.9% (3.2 → 3.9)
- anos_finais/inep/27: 2017→2019 variou +15.4% (3.9 → 4.5)
- anos_finais/inep/28: 2019→2021 variou +22.2% (3.6 → 4.4)
- anos_finais/inep/41: 2005→2007 variou +21.2% (3.3 → 4.0)
- anos_finais/inep/50: 2005→2007 variou +19.4% (3.1 → 3.7)
- anos_finais/inep/51: 2005→2007 variou +23.3% (3.0 → 3.7)
- anos_finais/inep/52: 2011→2013 variou +15.4% (3.9 → 4.5)
- medio/inep/11: 2007→2009 variou +19.4% (3.1 → 3.7)
- medio/inep/11: 2015→2017 variou +15.2% (3.3 → 3.8)
- medio/inep/13: 2005→2007 variou +21.7% (2.3 → 2.8)
- medio/inep/13: 2013→2015 variou +16.7% (3.0 → 3.5)
- medio/inep/15: 2007→2009 variou +30.4% (2.3 → 3.0)
- medio/inep/15: 2021→2023 variou +43.3% (3.0 → 4.3)
- medio/inep/16: 2021→2023 variou +16.1% (3.1 → 3.6)
- medio/inep/21: 2005→2007 variou +16.7% (2.4 → 2.8)
- medio/inep/24: 2023→2025 variou +21.9% (3.2 → 3.9)
- medio/inep/25: 2017→2019 variou +16.1% (3.1 → 3.6)
- medio/inep/26: 2011→2013 variou +16.1% (3.1 → 3.6)
- medio/inep/27: 2015→2017 variou +17.9% (2.8 → 3.3)
- medio/inep/28: 2015→2017 variou +19.2% (2.6 → 3.1)
- medio/inep/28: 2019→2021 variou +18.2% (3.3 → 3.9)
- medio/inep/29: 2017→2019 variou +18.5% (2.7 → 3.2)
- medio/inep/33: 2021→2023 variou -15.4% (3.9 → 3.3)
- medio/inep/41: 2017→2019 variou +18.9% (3.7 → 4.4)
- medio/inep/43: 2017→2019 variou +17.6% (3.4 → 4.0)
- medio/inep/43: 2023→2025 variou +20.5% (3.9 → 4.7)
- medio/inep/50: 2005→2007 variou +21.4% (2.8 → 3.4)
- medio/inep/51: 2005→2007 variou +15.4% (2.6 → 3.0)
- medio/inep/51: 2021→2023 variou +16.7% (3.6 → 4.2)
- medio/inep/52: 2009→2011 variou +16.1% (3.1 → 3.6)
- medio/inep/53: 2017→2019 variou +17.6% (3.4 → 4.0)

**Conferência com números publicados** (8)

- anos_iniciais/inep/BR/2025 (valor): 6.1 ≈ 6.1 ✓ (https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/ideb/ideb-avanca-em-todas-as-etapas-da-educacao-basica)
- anos_iniciais/inep/BR/2023 (valor): 5.7 ≈ 5.7 ✓ (https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/ideb/ideb-avanca-em-todas-as-etapas-da-educacao-basica)
- anos_finais/inep/BR/2025 (valor): 5.0 ≈ 5.0 ✓ (https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/ideb/ideb-avanca-em-todas-as-etapas-da-educacao-basica)
- anos_finais/inep/BR/2023 (valor): 4.7 ≈ 4.7 ✓ (https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/ideb/ideb-avanca-em-todas-as-etapas-da-educacao-basica)
- anos_iniciais/inep/22/2025 (valor): 6.1 ≈ 6.1 ✓ (https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/ideb/ideb-avanca-em-todas-as-etapas-da-educacao-basica-no-piaui)
- anos_finais/inep/22/2025 (valor): 5.2 ≈ 5.2 ✓ (https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/ideb/ideb-avanca-em-todas-as-etapas-da-educacao-basica-no-piaui)
- medio/inep/22/2025 (valor): 4.9 ≈ 4.9 ✓ (https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/ideb/ideb-avanca-em-todas-as-etapas-da-educacao-basica-no-piaui)
- medio/inep/22/2023 (valor): 4.3 ≈ 4.3 ✓ (https://www.gov.br/inep/pt-br/centrais-de-conteudo/noticias/ideb/ideb-avanca-em-todas-as-etapas-da-educacao-basica-no-piaui)

## `esperanca_vida` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | Estimativa IBGE (2000–2024) | 2000–2024 | — | estimativa: 700 |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (36)

- principal/projecoes2024/11: 2019→2020 variou -3.2% (76.57 → 74.15)
- principal/projecoes2024/11: 2020→2021 variou -4.9% (74.15 → 70.54)
- principal/projecoes2024/11: 2021→2022 variou +6.2% (70.54 → 74.94)
- principal/projecoes2024/12: 2021→2022 variou +5.6% (71.23 → 75.2)
- principal/projecoes2024/13: 2019→2020 variou -4.7% (75.34 → 71.81)
- principal/projecoes2024/13: 2021→2022 variou +7.3% (69.72 → 74.82)
- principal/projecoes2024/14: 2019→2020 variou -3.6% (74.12 → 71.42)
- principal/projecoes2024/14: 2020→2021 variou -3.3% (71.42 → 69.07)
- principal/projecoes2024/14: 2021→2022 variou +6.2% (69.07 → 73.32)
- principal/projecoes2024/15: 2019→2020 variou -3.2% (75.69 → 73.3)
- principal/projecoes2024/16: 2019→2020 variou -4.4% (73.95 → 70.69)
- principal/projecoes2024/16: 2021→2022 variou +4.5% (70.45 → 73.64)
- principal/projecoes2024/17: 2020→2021 variou -3.6% (75.24 → 72.52)
- principal/projecoes2024/17: 2021→2022 variou +4.0% (72.52 → 75.4)
- principal/projecoes2024/23: 2019→2020 variou -3.4% (76.78 → 74.19)
- principal/projecoes2024/23: 2021→2022 variou +3.2% (73.54 → 75.88)
- principal/projecoes2024/31: 2020→2021 variou -3.5% (76.67 → 73.98)
- principal/projecoes2024/31: 2021→2022 variou +3.4% (73.98 → 76.51)
- principal/projecoes2024/32: 2021→2022 variou +3.5% (73.75 → 76.31)
- principal/projecoes2024/33: 2021→2022 variou +4.5% (71.49 → 74.74)
- principal/projecoes2024/35: 2020→2021 variou -3.5% (75.55 → 72.9)
- principal/projecoes2024/35: 2021→2022 variou +4.2% (72.9 → 75.93)
- principal/projecoes2024/41: 2020→2021 variou -5.2% (75.82 → 71.91)
- principal/projecoes2024/41: 2021→2022 variou +4.8% (71.91 → 75.38)
- principal/projecoes2024/42: 2020→2021 variou -3.5% (77.23 → 74.52)
- principal/projecoes2024/42: 2021→2022 variou +3.2% (74.52 → 76.92)
- principal/projecoes2024/43: 2020→2021 variou -3.9% (76.27 → 73.29)
- principal/projecoes2024/50: 2020→2021 variou -4.6% (74.78 → 71.34)
- principal/projecoes2024/50: 2021→2022 variou +4.5% (71.34 → 74.53)
- principal/projecoes2024/51: 2019→2020 variou -3.3% (75.91 → 73.43)
- principal/projecoes2024/51: 2020→2021 variou -3.4% (73.43 → 70.96)
- principal/projecoes2024/51: 2021→2022 variou +5.6% (70.96 → 74.91)
- principal/projecoes2024/52: 2020→2021 variou -3.7% (74.46 → 71.68)
- principal/projecoes2024/52: 2021→2022 variou +5.3% (71.68 → 75.45)
- principal/projecoes2024/53: 2021→2022 variou +5.1% (74.95 → 78.78)
- principal/projecoes2024/BR: 2021→2022 variou +3.7% (72.78 → 75.45)

**Conferência com números publicados** (4)

- principal/projecoes2024/BR/2024 (valor): 76.61 ≈ 76.6 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024)
- principal/projecoes2024/BR/2021 (valor): 72.78 ≈ 72.8 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024)
- principal/projecoes2024/BR/2010 (valor): 74.36 ≈ 74.4 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024)
- principal/projecoes2024/BR/2000 (valor): 71.1 ≈ 71.1 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024)

## `mort_infantil` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | Estimativa IBGE (2000–2024) | 2000–2024 | — | estimativa: 700 |
| principal | Taxa direta DATASUS (referência) | 2000–2024 | — | — |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (83)

- principal/projecoes2024/11: 2010→2011 variou -23.6% (19.39 → 14.82)
- principal/projecoes2024/12: 2000→2001 variou -26.8% (36.89 → 27.02)
- principal/projecoes2024/12: 2002→2003 variou -15.1% (27.47 → 23.33)
- principal/projecoes2024/12: 2005→2006 variou -19.9% (27.5 → 22.03)
- principal/projecoes2024/12: 2006→2007 variou +15.8% (22.03 → 25.51)
- principal/projecoes2024/12: 2007→2008 variou -16.3% (25.51 → 21.36)
- principal/projecoes2024/12: 2015→2016 variou -19.1% (17.54 → 14.19)
- principal/projecoes2024/12: 2017→2018 variou +17.3% (14.84 → 17.4)
- principal/projecoes2024/12: 2020→2021 variou +30.6% (14.89 → 19.44)
- principal/projecoes2024/12: 2021→2022 variou -15.4% (19.44 → 16.45)
- principal/projecoes2024/13: 2006→2007 variou -15.1% (25.04 → 21.26)
- principal/projecoes2024/14: 2001→2002 variou -27.9% (21.19 → 15.28)
- principal/projecoes2024/14: 2002→2003 variou +38.7% (15.28 → 21.19)
- principal/projecoes2024/14: 2006→2007 variou -16.7% (22.15 → 18.45)
- principal/projecoes2024/14: 2008→2009 variou -16.8% (20.3 → 16.89)
- principal/projecoes2024/14: 2009→2010 variou -19.6% (16.89 → 13.58)
- principal/projecoes2024/14: 2011→2012 variou +27.7% (14.07 → 17.97)
- principal/projecoes2024/14: 2017→2018 variou +30.8% (17.13 → 22.4)
- principal/projecoes2024/14: 2018→2019 variou -20.5% (22.4 → 17.8)
- principal/projecoes2024/14: 2022→2023 variou +16.3% (19.17 → 22.29)
- principal/projecoes2024/16: 2014→2015 variou -18.1% (19.92 → 16.32)
- principal/projecoes2024/16: 2015→2016 variou +15.1% (16.32 → 18.78)
- principal/projecoes2024/16: 2018→2019 variou -15.8% (20.67 → 17.4)
- principal/projecoes2024/17: 2020→2021 variou +17.7% (10.75 → 12.65)
- principal/projecoes2024/21: 2005→2006 variou -20.6% (33.42 → 26.55)
- principal/projecoes2024/23: 2004→2005 variou -16.2% (28.75 → 24.1)
- principal/projecoes2024/24: 2002→2003 variou -16.6% (37.93 → 31.63)
- principal/projecoes2024/24: 2005→2006 variou -21.2% (26.6 → 20.96)
- principal/projecoes2024/25: 2000→2001 variou -19.9% (47.59 → 38.13)
- principal/projecoes2024/25: 2003→2004 variou -16.7% (35.12 → 29.25)
- principal/projecoes2024/25: 2008→2009 variou -16.7% (21.12 → 17.6)
- principal/projecoes2024/25: 2014→2015 variou -15.8% (14.61 → 12.3)
- principal/projecoes2024/26: 2003→2004 variou -19.8% (32.8 → 26.32)
- principal/projecoes2024/27: 2003→2004 variou -22.0% (37.14 → 28.97)
- principal/projecoes2024/27: 2005→2006 variou -16.9% (30.07 → 24.98)
- principal/projecoes2024/27: 2020→2021 variou +15.3% (11.88 → 13.7)
- principal/projecoes2024/28: 2006→2007 variou -20.1% (26.01 → 20.77)
- principal/projecoes2024/28: 2008→2009 variou -16.0% (21.03 → 17.67)
- principal/projecoes2024/32: 2008→2009 variou -17.5% (14.12 → 11.65)
- principal/projecoes2024/32: 2020→2021 variou +15.9% (9.93 → 11.51)
- principal/projecoes2024/41: 2000→2001 variou -16.7% (20.11 → 16.75)
- principal/projecoes2024/42: 2016→2017 variou +19.0% (8.65 → 10.29)
- principal/projecoes2024/50: 2001→2002 variou -15.9% (23.42 → 19.69)
- principal/projecoes2024/50: 2009→2010 variou -17.5% (18.22 → 15.03)
- principal/projecoes2024/51: 2005→2006 variou -20.8% (24.79 → 19.63)
- principal/projecoes2024/51: 2009→2010 variou -16.2% (18.54 → 15.53)
- principal/projecoes2024/53: 2018→2019 variou -21.3% (10.43 → 8.21)
- principal/projecoes2024/53: 2019→2020 variou +22.9% (8.21 → 10.09)
- principal/datasus_direta/11: 2007→2008 variou -16.1% (19.39 → 16.27)
- principal/datasus_direta/11: 2010→2011 variou -28.2% (18.54 → 13.31)
- principal/datasus_direta/12: 2000→2001 variou -22.9% (31.26 → 24.1)
- principal/datasus_direta/12: 2007→2008 variou -19.1% (22.12 → 17.89)
- principal/datasus_direta/12: 2010→2011 variou -17.4% (17.4 → 14.37)
- principal/datasus_direta/12: 2017→2018 variou +21.1% (13.63 → 16.5)
- principal/datasus_direta/14: 2001→2002 variou -23.4% (16.98 → 13.01)
- principal/datasus_direta/14: 2002→2003 variou +21.8% (13.01 → 15.85)
- principal/datasus_direta/14: 2003→2004 variou +21.1% (15.85 → 19.2)
- principal/datasus_direta/14: 2005→2006 variou +17.2% (18.05 → 21.16)
- principal/datasus_direta/14: 2006→2007 variou -19.1% (21.16 → 17.12)
- principal/datasus_direta/14: 2009→2010 variou -29.3% (18.3 → 12.94)
- principal/datasus_direta/14: 2011→2012 variou +30.3% (12.67 → 16.51)
- principal/datasus_direta/14: 2012→2013 variou +17.1% (16.51 → 19.33)
- principal/datasus_direta/14: 2014→2015 variou -17.3% (20.23 → 16.74)
- principal/datasus_direta/14: 2022→2023 variou +27.1% (18.79 → 23.88)
- principal/datasus_direta/14: 2023→2024 variou -20.0% (23.88 → 19.11)
- principal/datasus_direta/16: 2022→2023 variou +15.8% (18.07 → 20.93)
- principal/datasus_direta/17: 2020→2021 variou +18.5% (10.62 → 12.59)
- principal/datasus_direta/23: 2000→2001 variou -19.8% (26.51 → 21.26)
- principal/datasus_direta/23: 2004→2005 variou -18.4% (22.45 → 18.32)
- principal/datasus_direta/23: 2009→2010 variou -15.4% (15.52 → 13.13)
- principal/datasus_direta/24: 2002→2003 variou -17.5% (21.16 → 17.45)
- principal/datasus_direta/25: 2000→2001 variou -34.0% (32.18 → 21.23)
- principal/datasus_direta/25: 2021→2022 variou +16.5% (12.63 → 14.72)
- principal/datasus_direta/28: 2021→2022 variou +25.6% (14.04 → 17.63)
- principal/datasus_direta/28: 2023→2024 variou -24.4% (18.48 → 13.98)
- principal/datasus_direta/32: 2008→2009 variou -17.3% (14.5 → 11.99)
- principal/datasus_direta/32: 2020→2021 variou +15.2% (9.76 → 11.24)
- principal/datasus_direta/43: 2019→2020 variou -18.6% (10.62 → 8.64)
- principal/datasus_direta/50: 2001→2002 variou -15.3% (24.01 → 20.33)
- principal/datasus_direta/50: 2010→2011 variou -16.0% (15.72 → 13.21)
- principal/datasus_direta/50: 2016→2017 variou -18.1% (12.91 → 10.57)
- principal/datasus_direta/50: 2021→2022 variou +15.5% (10.69 → 12.35)
- principal/datasus_direta/53: 2018→2019 variou -16.8% (10.25 → 8.53)

**Conferência com números publicados** (4)

- principal/projecoes2024/BR/2024 (valor): 12.25 ≈ 12.3 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024)
- principal/projecoes2024/BR/2021 (valor): 12.17 ≈ 12.2 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024)
- principal/projecoes2024/BR/2010 (valor): 14.99 ≈ 15.0 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024)
- principal/projecoes2024/BR/2000 (valor): 28.13 ≈ 28.1 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024)

## `esgoto` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | PNAD (2001–2015) | 2001–2009, 2011–2015 | 2010 | baixa_precisao: 106, cobertura_urbana: 18 |
| principal | PNAD Contínua (2016–2018) | 2016–2018 | — | baixa_precisao: 8 |
| principal | PNAD Contínua (2019–) | 2019–2025 | — | — |

**Lacunas pontuais**

- principal/pnadc2019/11/2020: valor não publicado pelo IBGE
- principal/pnadc2019/11/2021: valor não publicado pelo IBGE
- principal/pnadc2019/12/2020: valor não publicado pelo IBGE
- principal/pnadc2019/12/2021: valor não publicado pelo IBGE
- principal/pnadc2019/13/2020: valor não publicado pelo IBGE
- principal/pnadc2019/13/2021: valor não publicado pelo IBGE
- principal/pnadc2019/14/2020: valor não publicado pelo IBGE
- principal/pnadc2019/14/2021: valor não publicado pelo IBGE
- principal/pnadc2019/15/2020: valor não publicado pelo IBGE
- principal/pnadc2019/15/2021: valor não publicado pelo IBGE
- principal/pnadc2019/16/2020: valor não publicado pelo IBGE
- principal/pnadc2019/16/2021: valor não publicado pelo IBGE
- principal/pnadc2019/17/2020: valor não publicado pelo IBGE
- principal/pnadc2019/17/2021: valor não publicado pelo IBGE
- principal/pnadc2019/21/2020: valor não publicado pelo IBGE
- principal/pnadc2019/21/2021: valor não publicado pelo IBGE
- principal/pnadc2019/22/2020: valor não publicado pelo IBGE
- principal/pnadc2019/22/2021: valor não publicado pelo IBGE
- principal/pnadc2019/23/2020: valor não publicado pelo IBGE
- principal/pnadc2019/23/2021: valor não publicado pelo IBGE
- principal/pnadc2019/24/2020: valor não publicado pelo IBGE
- principal/pnadc2019/24/2021: valor não publicado pelo IBGE
- principal/pnadc2019/25/2020: valor não publicado pelo IBGE
- principal/pnadc2019/25/2021: valor não publicado pelo IBGE
- principal/pnadc2019/26/2020: valor não publicado pelo IBGE
- principal/pnadc2019/26/2021: valor não publicado pelo IBGE
- principal/pnadc2019/27/2020: valor não publicado pelo IBGE
- principal/pnadc2019/27/2021: valor não publicado pelo IBGE
- principal/pnadc2019/28/2020: valor não publicado pelo IBGE
- principal/pnadc2019/28/2021: valor não publicado pelo IBGE
- principal/pnadc2019/29/2020: valor não publicado pelo IBGE
- principal/pnadc2019/29/2021: valor não publicado pelo IBGE
- principal/pnadc2019/31/2020: valor não publicado pelo IBGE
- principal/pnadc2019/31/2021: valor não publicado pelo IBGE
- principal/pnadc2019/32/2020: valor não publicado pelo IBGE
- principal/pnadc2019/32/2021: valor não publicado pelo IBGE
- principal/pnadc2019/33/2020: valor não publicado pelo IBGE
- principal/pnadc2019/33/2021: valor não publicado pelo IBGE
- principal/pnadc2019/35/2020: valor não publicado pelo IBGE
- principal/pnadc2019/35/2021: valor não publicado pelo IBGE
- principal/pnadc2019/41/2020: valor não publicado pelo IBGE
- principal/pnadc2019/41/2021: valor não publicado pelo IBGE
- principal/pnadc2019/42/2020: valor não publicado pelo IBGE
- principal/pnadc2019/42/2021: valor não publicado pelo IBGE
- principal/pnadc2019/43/2020: valor não publicado pelo IBGE
- principal/pnadc2019/43/2021: valor não publicado pelo IBGE
- principal/pnadc2019/50/2020: valor não publicado pelo IBGE
- principal/pnadc2019/50/2021: valor não publicado pelo IBGE
- principal/pnadc2019/51/2020: valor não publicado pelo IBGE
- principal/pnadc2019/51/2021: valor não publicado pelo IBGE
- principal/pnadc2019/52/2020: valor não publicado pelo IBGE
- principal/pnadc2019/52/2021: valor não publicado pelo IBGE
- principal/pnadc2019/53/2020: valor não publicado pelo IBGE
- principal/pnadc2019/53/2021: valor não publicado pelo IBGE
- principal/pnadc2019/BR/2020: valor não publicado pelo IBGE
- principal/pnadc2019/BR/2021: valor não publicado pelo IBGE

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (94)

- principal/pnad/11: 2002→2003 variou +48.1% (4.37 → 6.47)
- principal/pnad/11: 2003→2004 variou -31.1% (6.47 → 4.46)
- principal/pnad/11: 2007→2008 variou -24.5% (5.06 → 3.82)
- principal/pnad/11: 2008→2009 variou +61.5% (3.82 → 6.17)
- principal/pnad/11: 2009→2011 variou -20.1% (6.17 → 4.93)
- principal/pnad/11: 2011→2012 variou +71.4% (4.93 → 8.45)
- principal/pnad/11: 2012→2013 variou +63.0% (8.45 → 13.77)
- principal/pnad/11: 2013→2014 variou +21.7% (13.77 → 16.76)
- principal/pnad/12: 2003→2004 variou -26.0% (40.77 → 30.18)
- principal/pnad/12: 2014→2015 variou +30.3% (36.3 → 47.3)
- principal/pnad/13: 2001→2002 variou -24.4% (12.24 → 9.25)
- principal/pnad/13: 2002→2003 variou -22.6% (9.25 → 7.16)
- principal/pnad/13: 2003→2004 variou +45.7% (7.16 → 10.43)
- principal/pnad/13: 2004→2005 variou -54.3% (10.43 → 4.77)
- principal/pnad/13: 2005→2006 variou +34.0% (4.77 → 6.39)
- principal/pnad/13: 2006→2007 variou +408.0% (6.39 → 32.46)
- principal/pnad/13: 2008→2009 variou -25.6% (27.41 → 20.4)
- principal/pnad/13: 2009→2011 variou +84.8% (20.4 → 37.69)
- principal/pnad/14: 2001→2002 variou +129.8% (13.49 → 31.0)
- principal/pnad/14: 2002→2003 variou -43.8% (31.0 → 17.42)
- principal/pnad/14: 2004→2005 variou -24.0% (16.36 → 12.43)
- principal/pnad/14: 2005→2006 variou +28.8% (12.43 → 16.01)
- principal/pnad/14: 2007→2008 variou +43.7% (13.81 → 19.84)
- principal/pnad/14: 2008→2009 variou -33.0% (19.84 → 13.29)
- principal/pnad/14: 2009→2011 variou +148.8% (13.29 → 33.07)
- principal/pnad/14: 2011→2012 variou -25.2% (33.07 → 24.75)
- principal/pnad/14: 2014→2015 variou +60.0% (26.19 → 41.91)
- principal/pnad/15: 2003→2004 variou -36.2% (16.95 → 10.81)
- principal/pnad/15: 2009→2011 variou +66.6% (11.58 → 19.29)
- principal/pnad/15: 2011→2012 variou -27.2% (19.29 → 14.04)
- principal/pnad/16: 2001→2002 variou +181.2% (5.65 → 15.89)
- principal/pnad/16: 2002→2003 variou -62.7% (15.89 → 5.92)
- principal/pnad/16: 2004→2005 variou -66.2% (5.68 → 1.92)
- principal/pnad/16: 2005→2006 variou +51.6% (1.92 → 2.91)
- principal/pnad/16: 2006→2007 variou +26.8% (2.91 → 3.69)
- principal/pnad/16: 2007→2008 variou +38.8% (3.69 → 5.12)
- principal/pnad/16: 2008→2009 variou -75.0% (5.12 → 1.28)
- principal/pnad/16: 2009→2011 variou +471.1% (1.28 → 7.31)
- principal/pnad/16: 2012→2013 variou -55.9% (7.51 → 3.31)
- principal/pnad/16: 2013→2014 variou +269.8% (3.31 → 12.24)
- principal/pnad/16: 2014→2015 variou -61.0% (12.24 → 4.77)
- principal/pnad/17: 2002→2003 variou +34.0% (6.76 → 9.06)
- principal/pnad/17: 2003→2004 variou -23.5% (9.06 → 6.93)
- principal/pnad/17: 2004→2005 variou +27.8% (6.93 → 8.86)
- principal/pnad/17: 2005→2006 variou +35.8% (8.86 → 12.03)
- principal/pnad/17: 2006→2007 variou +20.9% (12.03 → 14.54)
- principal/pnad/17: 2007→2008 variou +31.6% (14.54 → 19.14)
- principal/pnad/17: 2013→2014 variou +42.4% (19.1 → 27.2)
- principal/pnad/17: 2014→2015 variou +26.7% (27.2 → 34.45)
- principal/pnad/21: 2005→2006 variou +26.5% (15.59 → 19.72)
- principal/pnad/21: 2008→2009 variou -20.2% (19.85 → 15.84)
- principal/pnad/21: 2009→2011 variou +55.7% (15.84 → 24.67)
- principal/pnad/21: 2012→2013 variou -28.7% (22.82 → 16.26)
- principal/pnad/21: 2014→2015 variou +50.3% (14.96 → 22.48)
- principal/pnad/22: 2001→2002 variou +55.8% (6.08 → 9.47)
- principal/pnad/22: 2002→2003 variou -26.5% (9.47 → 6.96)
- principal/pnad/22: 2006→2007 variou +88.1% (7.67 → 14.43)
- principal/pnad/22: 2007→2008 variou -51.7% (14.43 → 6.97)
- principal/pnad/22: 2011→2012 variou -43.0% (7.0 → 3.99)
- principal/pnad/22: 2013→2014 variou +87.2% (3.97 → 7.43)
- principal/pnad/22: 2014→2015 variou +27.3% (7.43 → 9.46)
- principal/pnad/23: 2001→2002 variou +20.9% (27.15 → 32.82)
- principal/pnad/24: 2003→2004 variou +30.8% (16.88 → 22.08)
- principal/pnad/24: 2011→2012 variou +20.9% (20.38 → 24.64)
- principal/pnad/25: 2009→2011 variou +33.1% (42.48 → 56.54)
- principal/pnad/26: 2009→2011 variou +36.0% (43.07 → 58.58)
- principal/pnad/27: 2003→2004 variou -36.6% (15.1 → 9.58)
- principal/pnad/27: 2004→2005 variou +36.0% (9.58 → 13.03)
- principal/pnad/27: 2007→2008 variou +40.7% (15.7 → 22.09)
- principal/pnad/27: 2008→2009 variou -26.5% (22.09 → 16.23)
- principal/pnad/27: 2009→2011 variou +98.8% (16.23 → 32.26)
- principal/pnad/27: 2012→2013 variou -31.6% (34.35 → 23.5)
- principal/pnad/27: 2013→2014 variou +25.3% (23.5 → 29.45)
- principal/pnad/27: 2014→2015 variou +26.1% (29.45 → 37.14)
- principal/pnad/28: 2003→2004 variou +23.8% (49.83 → 61.71)
- principal/pnad/50: 2001→2002 variou +32.8% (9.43 → 12.52)
- principal/pnad/50: 2005→2006 variou +29.1% (11.78 → 15.21)
- principal/pnad/50: 2006→2007 variou +33.7% (15.21 → 20.33)
- principal/pnad/50: 2009→2011 variou +59.6% (19.32 → 30.83)
- principal/pnad/50: 2011→2012 variou +31.7% (30.83 → 40.59)
- principal/pnad/50: 2014→2015 variou +31.3% (31.69 → 41.61)
- principal/pnad/51: 2001→2002 variou +25.0% (17.34 → 21.67)
- principal/pnad/51: 2007→2008 variou +87.8% (13.99 → 26.27)
- principal/pnad/51: 2008→2009 variou -40.3% (26.27 → 15.69)
- principal/pnad/51: 2009→2011 variou +50.9% (15.69 → 23.68)
- principal/pnadc2016/14: 2017→2018 variou +47.5% (27.8 → 41.0)
- principal/pnadc2016/15: 2017→2018 variou +23.1% (12.1 → 14.9)
- principal/pnadc2016/16: 2017→2018 variou +21.8% (11.0 → 13.4)
- principal/pnadc2016/22: 2017→2018 variou -20.8% (9.6 → 7.6)
- principal/pnadc2019/11: 2022→2023 variou +22.6% (23.4 → 28.7)
- principal/pnadc2019/11: 2023→2024 variou -36.9% (28.7 → 18.1)
- principal/pnadc2019/16: 2022→2023 variou +23.8% (21.0 → 26.0)
- principal/pnadc2019/16: 2023→2024 variou -31.5% (26.0 → 17.8)
- principal/pnadc2019/22: 2024→2025 variou +43.0% (13.5 → 19.3)

**Conferência com números publicados** (8)

- principal/pnadc2019/BR/2025 (valor): 71.4 ≈ 71.4 ✓ (https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/46449-domicilios-alugados-cresceram-mais-de-50-desde-2016)
- principal/pnadc2019/BR/2024 (valor): 70.4 ≈ 70.4 ✓ (https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/15ec1d59965a24b0bb2817eaf9b6f490.pdf)
- principal/pnadc2019/BR/2019 (valor): 68.1 ≈ 68.1 ✓ (https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/15ec1d59965a24b0bb2817eaf9b6f490.pdf)
- principal/pnadc2019/35/2024 (valor): 94.1 ≈ 94.1 ✓ (https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/15ec1d59965a24b0bb2817eaf9b6f490.pdf)
- principal/pnadc2019/22/2024 (valor): 13.5 ≈ 13.5 ✓ (https://agenciadenoticias.ibge.gov.br/media/com_mediaibge/arquivos/15ec1d59965a24b0bb2817eaf9b6f490.pdf)
- principal/pnad/BR/2015 (auxiliar sidra1956_rede_mil): 44454.83 ≈ 44455 ✓ (https://sidra.ibge.gov.br/tabela/1956)
- principal/pnad/43/2009 (auxiliar sidra1956_rede_mil): 1983.43 ≈ 1984 ✓ (https://sidra.ibge.gov.br/tabela/1956)
- principal/pnad/16/2014 (auxiliar sidra1956_rede_mil): 24.27 ≈ 24 ✓ (https://sidra.ibge.gov.br/tabela/1956)

## `homicidios` — OK

| Subindicador | Segmento | Anos | Lacunas do segmento | Flags |
|---|---|---|---|---|
| principal | SIM/DATASUS (2000–2024) | 2000–2024 | — | — |

**Erros** (0)

- nenhum

**Alertas (variação suspeita — revisar)** (15)

- principal/sim/12: 2015→2016 variou +65.4% (26.25 → 43.41)
- principal/sim/12: 2016→2017 variou +40.8% (43.41 → 61.1)
- principal/sim/13: 2020→2021 variou +35.7% (32.17 → 43.65)
- principal/sim/14: 2011→2012 variou +47.8% (19.73 → 29.16)
- principal/sim/14: 2012→2013 variou +44.8% (29.16 → 42.21)
- principal/sim/14: 2017→2018 variou +60.3% (43.97 → 70.47)
- principal/sim/14: 2018→2019 variou -46.3% (70.47 → 37.86)
- principal/sim/16: 2022→2023 variou +43.5% (45.01 → 64.57)
- principal/sim/21: 2000→2001 variou +57.9% (5.96 → 9.41)
- principal/sim/23: 2011→2012 variou +36.7% (32.5 → 44.43)
- principal/sim/23: 2016→2017 variou +48.3% (41.05 → 60.88)
- principal/sim/23: 2018→2019 variou -51.0% (54.59 → 26.75)
- principal/sim/23: 2019→2020 variou +64.2% (26.75 → 43.92)
- principal/sim/33: 2018→2019 variou -45.1% (37.64 → 20.66)
- principal/sim/33: 2019→2020 variou +35.8% (20.66 → 28.05)

**Conferência com números publicados** (6)

- principal/sim/BR/2024 (contagem): 42590.0 ≈ 42590 ✓ (https://repositorio.ipea.gov.br/entities/publication/9ab87dfc-33eb-4ac2-8a54-f4f1543dabbc)
- principal/sim/BR/2014 (contagem): 60474.0 ≈ 60474 ✓ (https://repositorio.ipea.gov.br/entities/publication/9ab87dfc-33eb-4ac2-8a54-f4f1543dabbc)
- principal/sim/28/2024 (contagem): 526.0 ≈ 526 ✓ (https://repositorio.ipea.gov.br/entities/publication/9ab87dfc-33eb-4ac2-8a54-f4f1543dabbc)
- principal/sim/16/2023 (contagem): 516.0 ≈ 516 ✓ (https://repositorio.ipea.gov.br/entities/publication/9ab87dfc-33eb-4ac2-8a54-f4f1543dabbc)
- principal/sim/35/2014 (contagem): 6185.0 ≈ 6185 ✓ (https://repositorio.ipea.gov.br/entities/publication/9ab87dfc-33eb-4ac2-8a54-f4f1543dabbc)
- principal/sim/14/2018 (contagem): 414.0 ≈ 414 ✓ (https://repositorio.ipea.gov.br/entities/publication/9ab87dfc-33eb-4ac2-8a54-f4f1543dabbc)
