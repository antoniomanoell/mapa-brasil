# Metodologia

Este site mostra indicadores socioeconômicos dos 26 estados e do Distrito Federal, de 2000 (ou do primeiro ano que cada fonte oficial publica) até o dado mais recente, usando somente fontes oficiais. Esta página explica como os números chegam ao mapa.

## De onde vêm os dados

Cada indicador vem de um órgão oficial: IBGE, INEP, Ministério da Saúde (DATASUS) e o PNUD, com o Ipea e a Fundação João Pinheiro (no IDHM). A página "Sobre o indicador" de cada um traz a fonte, a tabela usada e a data em que os dados foram extraídos.

A ordem de preferência é:

1. tabela publicada pelo próprio órgão produtor;
2. série oficial redistribuída por outro órgão público, só quando é idêntica à do produtor;
3. cálculo a partir dos microdados, só quando não existe tabela publicada. Nesse caso o cálculo é conferido contra números que o órgão publicou. Hoje isso acontece só na renda per capita, no Gini e no analfabetismo de 2001 a 2015, calculados com os microdados da PNAD anual.

## Como os números são conferidos

Antes de ir para o site, cada indicador passa por checagens automáticas:

- todos os estados e o Brasil presentes em todos os anos (ou a ausência explicada);
- valores dentro de faixas plausíveis;
- nenhum ano que ainda não terminou e nenhum dado preliminar;
- pelo menos três valores comparados com números divulgados oficialmente, que precisam coincidir, com diferença só de arredondamento, incluindo o Brasil no ano mais recente.

Se alguma checagem falha, o indicador não é atualizado no site até o problema ser resolvido.

Variações muito grandes de um ano para outro (o limite depende do indicador, de 8% a 35%) geram alertas, revisados por uma pessoa.

## Mudanças de metodologia: séries separadas

Quando uma pesquisa muda (por exemplo, quando a PNAD anual deu lugar à PNAD Contínua), os números de antes e de depois **não são emendados**. Emendar exigiria ajustar uma série para encaixar na outra, o que cria números que nenhum órgão oficial publicou.

As séries aparecem separadas: no gráfico, cada uma tem sua própria linha, e a quebra é marcada com uma linha vertical e uma nota (ⓘ) abaixo do gráfico; no mapa, o rótulo ao lado do seletor de ano diz de qual série é o valor. Quando duas séries cobrem o mesmo ano, as duas aparecem no gráfico, e ao lado do seletor de ano você escolhe qual ver no mapa.

## Lacunas

Ano sem dado fica sem dado: aparece em cinza hachurado no mapa (passando o mouse, aparece o motivo, quando conhecido), como "sem dado" na tabela e como interrupção na linha do gráfico. Nenhum valor é inventado, interpolado ou repetido do ano anterior.

Exceção: em séries publicadas a cada dois anos, como o Ideb, os pontos são ligados por uma linha tracejada só para guiar o olho; não há valor entre eles.

## Projeções e estimativas

Não há projeções para o futuro. Valores que são estimativas de um modelo (como a esperança de vida e a mortalidade infantil do IBGE) aparecem com o aviso "valores estimados, não medidos" no painel do estado. Embora venham das Projeções da População do IBGE, só entram anos já encerrados, cujos valores coincidem com as Tábuas de Mortalidade publicadas pelo IBGE.

## Valores em dinheiro

Dentro de cada indicador, os valores em reais estão em reais de um mesmo ano, para que anos diferentes possam ser comparados; o ano aparece na legenda do mapa e no painel do estado. Cada indicador segue o método da sua fonte: a renda é corrigida pelo IPCA e mostrada por mês; o PIB é corrigido pelos índices de preços das Contas Regionais e mostrado por ano. Por isso, os valores de renda e de PIB não devem ser comparados diretamente.

## População

Todas as taxas calculadas pelo site (homicídios por 100 mil habitantes, PIB per capita) usam a mesma série de população: as Projeções da População do IBGE (Revisão 2024), uma série única e consistente de 2000 em diante, sem os saltos que aparecem quando se juntam estimativas feitas em épocas diferentes.

Por isso, essas duas taxas podem diferir um pouco das divulgadas por outras fontes que usam outra população: o Atlas da Violência, nos homicídios, e a divulgação das Contas Regionais, no PIB per capita (que usa a população recenseada).

## Margem de erro

Indicadores que vêm de pesquisas por amostra (PNAD e PNAD Contínua) têm margem de erro. Quando a margem de erro é grande (coeficiente de variação acima de 15%), o valor aparece com aviso de "baixa precisão" no mapa, na tabela (asterisco) e no gráfico do estado (ponto vazado). Isso acontece sobretudo em estados pequenos e em indicadores de proporções baixas, como a extrema pobreza.

Nem toda fonte publica a margem de erro. Quando não publica (por exemplo, nas séries da PNAD anual de esgoto e Gini, e no IDHM), o site não tem como marcar valores imprecisos; neles, diferenças pequenas entre estados devem ser lidas com cautela.

## Cores do mapa

A escala de cores de cada indicador é calculada uma vez, sobre todos os anos juntos, e não muda quando você mexe no ano. Assim, a mudança de cor reflete mudança real. As cores dividem os valores em 5 faixas, cada uma com um quinto de todos os valores dos estados em todos os anos; os limites aparecem na legenda.

Num indicador que melhorou muito, os primeiros anos podem aparecer quase todos claros e os últimos quase todos escuros. Isso é a mudança ao longo do tempo, não um defeito do mapa. As cores mostram só a intensidade ("mais escuro = maior"), sem dizer se o valor é bom ou ruim. Em indicadores em que maior é pior (como homicídios ou mortalidade infantil), mais escuro significa pior.

## Mapa e ranking

O mapa dá mais destaque visual a estados de área grande, mesmo quando têm pouca população. O botão "Ranking", ao lado de "Mapa", mostra todos os estados em ordem, com o mesmo peso, e, junto com o seletor "Estado", é a forma de navegar pelo teclado. A lista vai sempre do maior para o menor valor; em indicadores em que maior é pior, como homicídios, os primeiros são os piores.
