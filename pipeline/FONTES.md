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
