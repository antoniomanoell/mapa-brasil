# REPORT do pipeline

- Data: 2026-10-21
- Versão do pipeline: `1122a52`
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
