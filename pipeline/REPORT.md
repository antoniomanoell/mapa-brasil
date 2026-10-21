# REPORT do pipeline

- Data: 2026-10-21
- Versão do pipeline: `4856c47`
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
