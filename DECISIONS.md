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
