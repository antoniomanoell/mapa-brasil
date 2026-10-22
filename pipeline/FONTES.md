# FONTES.md — fontes verificadas

Registro das fontes conferidas diretamente nas APIs e sites oficiais. Cada item diz o que foi
verificado e quando. Decisões metodológicas ficam em `../DECISIONS.md`.

## Geografia

**Malha das UFs** — verificado em 2026-10-20
- API v4 de malhas do IBGE: `https://servicodados.ibge.gov.br/api/v4/malhas/paises/BR?intrarregiao=UF&formato=application/json&qualidade=intermediaria&periodo=2025`
- Devolve TopoJSON direto (objeto `BRUF`, propriedade `codarea` = código da UF). 87 KB (30 KB gzip).
- Os arquivos de 2022 a 2025 são idênticos byte a byte.

**Códigos das UFs** — `https://servicodados.ibge.gov.br/api/v1/localidades/estados` (27 UFs, conferido em 2026-10-20).

## População (denominador único, seção 4.2)

**IBGE — Projeções da População, Revisão 2024** — verificado em 2026-10-20
- `https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2024/projecoes_2024_tab4_indicadores.xlsx`
- Aba `4) INDICADORES`, coluna `POP_T`, por ano (2000–2070) e local (`CÓD.` 0 = Brasil, 11–53 = UFs).
- A mesma aba traz `e0_T` (esperança de vida) e `TMI_T` (mortalidade infantil), úteis na Fase 3.
- Metodologia: `Serie_Relatorios_Metotodologicos_v40_..._Revisao_2024_3a_Edicao.pdf`, na mesma pasta.
- **O SIDRA não serve:** as tabelas 7358, 7360 e 7362 são da revisão 2018 (periodicidade 2018–2018).

## `homicidios`

**DATASUS — SIM, via TabNet** — verificado em 2026-10-20
- Formulário: `http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sim/cnv/obt10uf.def`
- Consulta (POST, latin-1): `http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sim/cnv/obt10uf.def`
  - `Linha=Unidade_da_Federação`, `Coluna=--Não-Ativa--`, `Incremento=Óbitos_p/Residênc`
  - `Arquivos=obtufAA.dbf` (um ano por consulta; há arquivos de 1996 a 2026)
  - `SGrupo_CID-10=246` (Agressões, X85–Y09) e `SGrupo_CID-10=248` (Intervenções legais e operações de guerra, Y35–Y36)
  - `formato=prn` devolve CSV com `;` dentro de `<PRE>`.
- O formulário diz: "Dados de 2025 - Preliminares - data de extração 28/07/2026". **Último ano consolidado: 2024.**
- Conferência: o total de 2024 pela consulta acima (42.590) é igual ao número de homicídios do
  Atlas da Violência 2026 (IPEA/FBSP, 26/05/2026). Isso confirma a definição X85–Y09 + Y35–Y36 por residência.
- O Atlas da Violência 2026 traz, na Tabela 2.2 (p. 17), as contagens por UF de 2014 a 2024, e as
  usamos na conferência: https://repositorio.ipea.gov.br/entities/publication/9ab87dfc-33eb-4ac2-8a54-f4f1543dabbc
- As **taxas** do Atlas usam outra série de população: com a revisão 2024 dá AP 45,2 contra 45,7 no
  Atlas, e BR 20,0 contra 20,1. SP, SC, DF e MG coincidem na 1ª casa decimal.

## `idhm`

**PNUD/IPEA/FJP — Atlas Brasil** — verificado em 2026-10-20
(links em `https://www.atlasbrasil.org.br/acervo/biblioteca`, seção "Bases de dados")
- Segmento Censo: `https://www.atlasbrasil.org.br/cockpit/storage/uploads/dados/censo_total_1991_2010.xlsx`
  - Abas `UF 91-00-10` e `BR 91-00-10`, colunas `IDHM`, `IDHM_E`, `IDHM_L`, `IDHM_R`; anos 1991, 2000, 2010.
  - Metadados: `.../censo_metadados_1991_2010.xlsx`
- Segmento PNADC (Radar IDHM): `https://www.atlasbrasil.org.br/cockpit/storage/uploads/dados/adh_radar_base_2012_2024.xlsx`
  - Aba `Total`: `ANO`, `AGREGACAO` (`Brasil` / `Unidade da Federação`), `CODIGO`, `IDHM`, `IDHM_L`, `IDHM_E`, `IDHM_R`.
  - 27 UFs, de 2012 a 2024, sem lacunas. A aba `Total B` tem conteúdo idêntico (motivo não documentado).
  - Os metadados (`.../adh_radar_metadados_2012_2024.xlsx`) dizem: visita 1 da PNADC em 2012–2019 e 2023;
    **visita 5 em 2020 e 2021**.
- Valores do Brasil publicados pelo PNUD e usados na conferência: 2012 = 0,744 e 2024 = 0,805 (geral);
  Educação 0,679 → 0,798; Longevidade 2024 = 0,860; Renda 0,732 → 0,760.
  Fontes: https://www.undp.org/pt/brazil/news/educacao-longevidade-e-retomada-da-renda-impulsionam-avanco-do-idhm-brasileiro
  e https://www.undp.org/pt/brazil/press-releases/brasil-alcanca-pela-primeira-vez-patamar-de-muito-alto-desenvolvimento-humano-aponta-pnud
- **Pendente:** falta conferência independente do segmento Censo (2000, 2010). Os PDFs de terceiros
  encontrados não abriram, e não há referência verificada.
- Publicação: "Radar IDHM: evolução do IDHM e de seus componentes — 2012 a 2024", PNUD, 26/05/2026,
  `https://www.undp.org/pt/brazil/publications/radar-idhm-evolucao-do-idhm-e-de-seus-componentes-periodo-de-2012-2024`

## `renda_pc`

**IBGE — PNAD Contínua anual (SIDRA)** — verificado em 2026-10-20
- Tabela **7533**: rendimento médio mensal real domiciliar per capita, **a preços médios do último ano**.
  - Variável 10816 (valor, R$) e 10817 (CV, %). Classificação 1019, categoria 49243 = Total.
  - Níveis N1, N2 e N3 (UF); anos 2012–2025.
- Tabela 7531: o mesmo a preços médios **do ano** (nominal), caso o deflacionamento seja feito pelo projeto.
- Informativo "Rendimento de todas as fontes 2025" (IBGE), na mesma série da 7533:
  `https://biblioteca.ibge.gov.br/visualizacao/livros/liv102275_informativo.pdf`
  - Deflator: **IPCA** (p. 1). Brasil a preços de 2025: 2019 = 1.904, 2024 = 2.118, 2025 = 2.264 (p. 13).
  - Visitas: **5ª visita em 2020–2022**; 1ª nos demais anos (notas das pp. 5, 7 e 10).
- **Atenção:** o IBGE divulga outro número, a "renda domiciliar per capita" para o FPE (R$ 2.316 em
  2025, nominal, release de 27/02/2026). É outro produto. Não confundir com a 7533.

**IBGE — PNAD anual 2001–2015 (SIDRA, pesquisa `PD`)**
- **Não há** tabela de rendimento domiciliar *per capita* médio por UF. As tabelas existentes trazem
  rendimento de pessoas (1860, 1862…), de domicílios (401, 430…) e o Gini de domicílios (403/573) ou
  de pessoas com rendimento (299). Nenhuma corresponde ao conceito do indicador.
- A tabela 573 confirma a cobertura da PNAD até 2003: "exceto a área rural de Rondônia, Acre, Amazonas,
  Roraima, Pará e Amapá".

**IBGE — PNAD anual, microdados (FTP)** — verificado em 2026-10-21
- `https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_anual/microdados/`
- 2001–2009, 2011 e 2012: `reponderacao_2001_2012/PNAD_reponderado_<ano>[_AAAAMMDD].zip`, com pesos
  recalibrados pela Projeção da População de 2013 (`nota_tecnica.pdf` na mesma pasta). Cada zip traz
  DOM/PES, dicionário e input SAS. A pasta `reponderacao_2001_2009/` usa a projeção de 2008 e está superada.
- 2013–2015: `<ano>/Dados_AAAAMMDD.zip` + `<ano>/Dicionarios_e_input_AAAAMMDD.zip`.
- As posições das variáveis mudam a cada ano; o pipeline as lê do input SAS. 2001–2003 não trazem o
  per capita pronto (V4621/V4742), então ele é calculado; de 2004 em diante o cálculo confere com o V4621.
- Espécie do domicílio (V0201), igual em todos os anos: 1 particular permanente, 3 particular
  improvisado, 5 coletivo.
- A nota técnica confirma a lista de UFs sem área rural até 2003: RO, AC, AM, RR, PA e AP.

**IBGE — Síntese de Indicadores Sociais 2016, Tabela 6.6** (conferência do segmento PNAD)
- `https://ftp.ibge.gov.br/Indicadores_Sociais/Sintese_de_Indicadores_Sociais/Sintese_de_Indicadores_Sociais_2016/xls/6_padrao_vida_distribuicao_renda_xls.zip`
- Rendimento domiciliar per capita médio e mediano, com CV, por UF, 2004–2009 e 2011–2015, a preços de
  setembro de 2015 (INPC). Conceito: média por arranjo domiciliar, **sem** os sem rendimento — difere da
  7533 (ver DECISIONS.md).

**Deflatores (SIDRA)**: IPCA = tabela 1737, variável 2266; INPC = tabela 1736, variável 2289
(números-índice mensais, dez/1993 = 100).

## `esperanca_vida` e `mort_infantil`

**IBGE — Projeções da População, Revisão 2024** (mesma planilha da população) — verificado em 2026-10-21
- Colunas `e0_T` (esperança de vida ao nascer) e `TMI_T` (mortalidade infantil, por mil nascidos vivos).
- Até 2024 coincidem com as **Tábuas Completas de Mortalidade 2024** (IBGE, 28/11/2025), inclusive na
  queda de 2020–2021. Brasil: e0 2000 = 71,1; 2010 = 74,4; 2021 = 72,8; 2024 = 76,6. TMI 2000 = 28,1;
  2010 = 15,0; 2021 = 12,2; 2024 = 12,3.
  Fonte: https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/45275-expectativa-de-vida-chega-a-76-6-anos-em-2024
- Valores de 2025 em diante são projeção e ficam de fora até sair a Tábua do ano (DECISIONS.md).

**DATASUS — taxa direta de mortalidade infantil (série de referência)** — verificado em 2026-10-21
- Óbitos de menores de 1 ano: SIM, `obt10uf.def`, filtro `SFaixa_Etária = 1` ("Menor 1 ano"), por residência.
- Nascidos vivos: SINASC, `http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sinasc/cnv/nvuf.def`,
  `Incremento=Nascim_p/resid.mãe`, arquivos `nvufAA.dbf`. O SINASC declara 2025 como preliminar.
- Brasil 2024: 30.020 óbitos ÷ 2.389.325 nascidos vivos = 12,56 por mil (estimativa IBGE: 12,3).

## `desocupacao` e `informalidade`

**IBGE — PNAD Contínua anual, mercado de trabalho (SIDRA)** — verificado em 2026-10-21
- Tabela **4562**: taxa de desocupação anual (var. 4099) e CV (var. 4103), 2012–2025, N1/N3.
- Tabela **4708**: taxa de informalidade anual (var. 12466) e CV (var. 12467), 2016–2025, N1/N3.
- A taxa anual não é a média dos trimestres (tabela 4099 trimestral): Brasil 2024 = 6,6% anual
  contra 6,85% na média dos 4 trimestres. O IBGE divulga a anual.
- Informalidade começa em 2016: a condição de CNPJ (empregador e conta própria) só tem médias anuais
  a partir de 2016 ("PNAD Contínua — retrospectiva 2012–2022", p. 15, 2012–2015 sem dado):
  https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Principais_destaques_PNAD_continua/2012_2022/PNAD_continua_retrospectiva_2012_2022.pdf
- Referências: https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/45920-pnad-continua-taxas-anuais-de-desocupacao-sao-as-menores-da-serie-em-20-unidades-da-federacao

## `gini`

- PNADC: SIDRA **7435** (var. 10681 índice, 10682 CV), 2012–2025. Brasil 2019 = 0,543; 2024 = 0,504;
  2025 = 0,511 (informativo Rendimento de todas as fontes 2025, pp. 1 e 14).
- PNAD 2001–2015: microdados (mesmo módulo da `renda_pc`), Gini ponderado da renda per capita por
  pessoa. O SIDRA não publica esse Gini por UF para a PNAD antiga; a SIS 2016 só publica o Gini do
  rendimento individual (Tabela 6.3, pessoas de 15+ com rendimento, V4720), que o mesmo código
  reproduz exatamente em 2015 (BR 0,491; SP 0,460; SC 0,419; PB 0,510; AL 0,438; RO 0,452; RJ 0,503).

## `analfabetismo`

- PNADC: SIDRA **7113** (var. 10267 taxa, 10268 CV), sexo Total (6794), "15 anos ou mais" (2795),
  2016–2025. Brasil 2024 = 5,3%; 2025 = 4,9% (notícias IBGE 43699 e 47221).
- PNAD 2001–2015: SIDRA **271** (pessoas de 5+ por alfabetização e grupo de idade). Taxa = não
  alfabetizadas ÷ (alfabetizadas + não) nos grupos 15–19, 20–24, 25–29, 30–39, 40–49, 50–59 e 60+
  (idade ignorada fora). Brasil 2015 = 7,95%, contra 8,0% na SIS 2016, Tabela 4.15.

## `esgoto`

- O IBGE divulga o indicador "domicílios com acesso à rede geral ou fossa séptica ligada à rede geral
  de esgoto" (informativo Características gerais dos domicílios 2024, pp. 35–36): Brasil 2019 = 68,1;
  2023 = 69,7; 2024 = 70,4; 2025 = 71,4 (notícia 46449). Por UF em 2024: SP 94,1 … PI 13,5.
- PNADC 2019+: SIDRA **7192**, var. 9988 (%), situação Total, categorias 47930 + 47931.
- PNADC 2016–2018: SIDRA **6735**, var. 9988/9989, categoria 46290 (rede geral, pluvial ou fossa
  ligada à rede). Categorias diferentes das de 2019+, por isso outro segmento.
- PNAD 2001–2015: SIDRA **1956**, var. 96 (domicílios particulares permanentes, mil), categorias
  99663 (rede coletora) + 9490 (fossa séptica ligada à rede coletora) ÷ 99662 (tinham banheiro).
- O denominador do IBGE são os domicílios com banheiro, sanitário ou buraco para dejeções.

## `pobreza` e `extrema_pobreza`

**IBGE — Síntese de Indicadores Sociais 2025** — verificado em 2026-10-21
- `2_Distribuicao_Renda_xls.zip`, **Tabela 2.23** ("Pobr_valor_Geo"): uma aba por ano (2012–2024) e
  outra com os CVs. Colunas "Proporção de pessoas com rendimento domiciliar per capita menor que
  US$ 2,15 / 3,65 / 6,85 PPC 2017 (%)". Linhas para Brasil, regiões, UFs e capitais.
- Visitas (rodapé de cada aba): 1ª visita, exceto 2020–2022 (5ª visita).
- Valores divulgados: Brasil 2024 = 23,1% (pobreza) e 3,5% (extrema); 2023 = 27,3% e 4,4%; 2012 =
  34,7% e 6,6% (notícia 45344; apresentação da SIS 2025, p. 43).
- O SIDRA tem os indicadores ODS 1.1.1 (5817) e 1.2.1 (5877), mas com **outras linhas**; não usar.
- A SIS 2025 não incorporou as linhas do Banco Mundial de junho de 2025; a próxima edição deve
  incorporar, e a série inteira muda.

## `pib_pc`

**IBGE — Contas Regionais do Brasil 2023 (referência 2010)** — verificado em 2026-10-21
- `Especiais_2002_2023_xls.zip`: **tab01** (PIB a preços correntes, R$ milhões) e **tab03** (série
  encadeada do volume do PIB, 2002 = 100), Brasil, regiões e UFs, 2002–2023.
- O SIDRA só tem o PIB corrente por UF (tabela 5938, PIB dos Municípios); não tem o volume.
- Notícia 45142: PIB 2023 SP = R$ 3.444.814 milhões, DF = R$ 365.669 milhões; crescimento real
  acumulado 2002–2023 BR 58,2%, RR 151,6%, MA 102,8%, SP 52,5%, DF 76,3% (reproduzidos exatamente).
- Per capita: Contas Nacionais (SIDRA 6784, var. 9812) Brasil 2023 = R$ 51.693,92, com a população
  das Projeções. A notícia das Contas Regionais usa a população recenseada (Brasil R$ 53.886,67).

## `ideb`

**INEP — Ideb 2025 (série 2005–2025)** — verificado em 2026-10-22
- Página: https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados
- `divulgacao_regioes_ufs_ideb_2025.zip` (abas "UF e Regiões (AI/AF/EM)") e
  `divulgacao_brasil_ideb_2025.zip` (abas "Brasil (...)"), Last-Modified 05/08/2026.
- Ideb observado nas colunas `VL_OBSERVADO_AAAA`. **Defeito do arquivo:** na aba "Brasil (Anos
  Finais)" a coluna de 2023 está sem código; o leitor usa o cabeçalho de texto "IDEB 2023 (N x P)".
- A planilha abrevia "R. G. do Norte", "R. G. do Sul" e "M. G. do Sul". Rótulos de rede trazem notas
  entre parênteses ("Pública (4)").
- Ensino médio por UF: só redes Total, Estadual e Privada.
- Referências: Brasil, rede pública, 2023 → 2025: anos iniciais 5,7 → 6,1; anos finais 4,7 → 5,0
  (notícia do INEP); Piauí 2025: 6,1 / 5,2 / 4,9 (notícia do INEP para o Piauí).
- O certificado TLS de download.inep.gov.br vem sem o intermediário; o pipeline valida pelo repositório
  do sistema (`truststore`), sem desligar a verificação.
