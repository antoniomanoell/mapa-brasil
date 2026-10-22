// Testes de fumaça (PROJECT.md, 5.1): carregar, trocar indicador, mover slider, clicar UF.

import { type Page, expect, test } from '@playwright/test';

async function abrir(page: Page, query = '') {
  await page.goto(`/${query}`);
  await expect(page.locator('body')).toHaveAttribute('data-pronto', 'true', { timeout: 60_000 });
}

test('carrega mapa, legenda e slider', async ({ page }) => {
  const erros: string[] = [];
  page.on('pageerror', (e) => erros.push(e.message));
  page.on('console', (m) => m.type() === 'error' && erros.push(m.text()));
  await abrir(page);
  await expect(page.locator('#mapa canvas')).toBeVisible();
  await expect(page.locator('#legenda')).toContainText('sem dado');
  await expect(page.locator('.slider-rotulo')).toContainText(/\d{4} · /);
  await expect(page).toHaveURL(/i=idhm/);
  expect(erros).toEqual([]);
  await page.screenshot({ path: `test-results/inicio-${test.info().project.name}.png` });
});

test('troca de indicador atualiza URL e título', async ({ page }) => {
  await abrir(page);
  await page.selectOption('#sel-indicador', 'renda_pc');
  await expect(page).toHaveURL(/i=renda_pc/);
  await expect(page).toHaveTitle(/Renda domiciliar per capita/);
  await expect(page.locator('#legenda')).toContainText('R$ de');
});

test('slider muda o ano e mostra o segmento', async ({ page }) => {
  await abrir(page, '?i=idhm');
  const range = page.locator('#slider input[type=range]');
  await range.fill('2010');
  await expect(page).toHaveURL(/a=2010/);
  await expect(page.locator('.slider-rotulo')).toHaveText('2010 · Censo (2000, 2010)');
  await range.fill('2005');
  await expect(page.locator('.slider-rotulo')).toHaveText('2005 · sem dado');
});

test('clicar numa UF do mapa abre o painel com o gráfico', async ({ page }) => {
  await abrir(page, '?i=homicidios');
  const centro = await page.evaluate(() =>
    (window as unknown as { __centroUF: (s: string) => { x: number; y: number } }).__centroUF('BA'),
  );
  const caixa = await page.locator('#mapa').boundingBox();
  if (!caixa) throw new Error('mapa sem caixa');
  await page.mouse.click(caixa.x + centro.x, caixa.y + centro.y);
  await expect(page).toHaveURL(/uf=BA/);
  const painel = page.locator('#painel');
  await expect(painel).toBeVisible();
  await expect(painel.locator('.painel-titulo')).toHaveText('Bahia');
  await expect(painel.locator('.grafico svg')).toBeVisible();
  await page.screenshot({ path: `test-results/painel-${test.info().project.name}.png` });
  await painel.locator('.fechar').click();
  await expect(painel).toBeHidden();
  await expect(page).not.toHaveURL(/uf=/);
});

test('ranking é navegável e abre o painel', async ({ page }) => {
  await abrir(page, '?i=renda_pc&v=ranking');
  const linhas = page.locator('table.ranking tbody tr');
  await expect(linhas).toHaveCount(27);
  await page.screenshot({ path: `test-results/ranking-${test.info().project.name}.png` });
  await linhas.first().locator('button').click();
  await expect(page.locator('#painel')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('#painel')).toBeHidden();
});

test('URL restaura a tela e parâmetros inválidos caem no padrão', async ({ page }) => {
  await abrir(page, '?i=idhm&s=educacao&a=2014&uf=se&v=ranking');
  await expect(page.locator('#sel-sub')).toHaveValue('educacao');
  await expect(page.locator('#ranking')).toBeVisible();
  await expect(page.locator('#painel .painel-titulo')).toHaveText('Sergipe');
  await abrir(page, '?i=xyz&a=1700&uf=ZZ&v=pizza');
  await expect(page).toHaveURL(/i=idhm/);
  await expect(page.locator('#mapa-area')).toBeVisible();
  await expect(page.locator('#painel')).toBeHidden();
});

test('cartões-resumo, recorte em botões e ranking ao lado do mapa no computador', async ({
  page,
}) => {
  await abrir(page, '?i=idhm&a=2024');
  const resumo = page.locator('#resumo');
  await expect(resumo.locator('.cartao-br')).toContainText('0,805');
  await expect(resumo.locator('.cartao-br')).toContainText('desde 2023');
  await expect(resumo).toContainText('Maior valor');
  await expect(resumo).toContainText('27 de 27 estados com dado');
  // Recortes do IDHM (4) viram botões; o seletor do cabeçalho some.
  const recortes = page.locator('#recortes button');
  await expect(recortes).toHaveCount(4);
  await expect(page.locator('#campo-sub')).toBeHidden();
  await recortes.filter({ hasText: 'Educação' }).click();
  await expect(page).toHaveURL(/s=educacao/);
  await expect(recortes.filter({ hasText: 'Educação' })).toHaveAttribute('aria-pressed', 'true');
  // Cartão de maior valor abre o painel do estado.
  await resumo.locator('button.cartao').nth(1).click();
  await expect(page.locator('#painel')).toBeVisible();
  const largo = (page.viewportSize()?.width ?? 0) >= 960;
  if (largo) {
    await expect(page.locator('#ranking')).toBeVisible();
    await expect(page.locator('#mapa-area')).toBeVisible();
  }
});

test('nada passa da largura da tela', async ({ page }) => {
  await abrir(page, '?i=idhm&uf=MA');
  const excesso = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(excesso).toBeLessThanOrEqual(0);
  const slider = await page.locator('#slider input[type=range]').boundingBox();
  expect(slider?.width ?? 0).toBeGreaterThan(100);
});

test('mortalidade infantil: estimativa no mapa, taxa direta só no painel', async ({ page }) => {
  await abrir(page, '?i=mort_infantil&uf=AM');
  await expect(page.locator('.slider-rotulo')).toContainText('Estimativa IBGE');
  const painel = page.locator('#painel');
  await expect(painel.locator('.painel-legenda')).toContainText('Taxa direta DATASUS (referência)');
  await expect(painel.locator('.painel-sub')).toContainText('valores estimados');
  await page.screenshot({ path: `test-results/mort-infantil-${test.info().project.name}.png` });
});

test('ideb: três etapas e pontos bienais ligados por tracejado', async ({ page }) => {
  await abrir(page, '?i=ideb&s=medio&uf=PI&a=2025');
  await expect(page.locator('#sel-sub option')).toHaveCount(3);
  await expect(page.locator('.slider-rotulo')).toContainText('2025 · INEP');
  const painel = page.locator('#painel');
  await expect(painel.locator('.painel-legenda')).toContainText('dado a cada dois anos');
  await expect(painel.locator('.painel-valores')).toContainText('4,9');
  await page.screenshot({ path: `test-results/ideb-${test.info().project.name}.png` });
});

test('página "Sobre o indicador" traz texto revisado e ficha técnica', async ({ page }) => {
  await page.goto('/indicador.html?i=homicidios');
  await expect(page.locator('body')).toHaveAttribute('data-pronto', 'true');
  await expect(page.locator('h1')).toHaveText('Taxa de homicídios');
  // Só o texto principal; a seção "Quem é responsável" tem a própria marca de revisão.
  await expect(page.locator('#conteudo > .aviso-rascunho')).toHaveCount(0);
  await expect(page.locator('#conteudo')).toContainText('O que mede');
  await expect(page.locator('#conteudo')).toContainText('Ficha técnica');
  await expect(page).toHaveTitle(/Sobre o indicador: Taxa de homicídios/);
});

test('metodologia, sobre e link a partir do mapa', async ({ page }) => {
  await page.goto('/metodologia.html');
  await expect(page.locator('h1')).toHaveText('Metodologia');
  await page.goto('/sobre.html');
  await expect(page.locator('h1')).toHaveText('Sobre');
  await abrir(page, '?i=gini');
  // "Sobre este indicador" abre uma gaveta na própria página, sem trocar de URL.
  await page.locator('#abrir-sobre').click();
  const gaveta = page.locator('#sobre-indicador');
  await expect(gaveta).toBeVisible();
  await expect(gaveta.locator('h2').first()).toContainText('Gini');
  await expect(gaveta).toContainText('O que mede');
  await expect(gaveta).toContainText('Ficha técnica');
  await expect(page).not.toHaveURL(/indicador\.html/);
  await page.keyboard.press('Escape');
  await expect(gaveta).toBeHidden();
  // O link do rodapé também abre a gaveta.
  await page.locator('#rodape-viz a', { hasText: 'Sobre este indicador' }).click();
  await expect(gaveta).toBeVisible();
});

test('seção "Quem é responsável" com base legal, só onde há texto', async ({ page }) => {
  await abrir(page, '?i=ideb');
  await page.locator('#abrir-sobre').click();
  const secao = page.locator('#sobre-indicador .competencias');
  await expect(secao.locator('h2')).toHaveText('Quem é responsável');
  await expect(secao).toContainText('não avalia governos');
  await expect(secao).toContainText('CF art. 211');
  await expect(secao).toContainText('Por Poder');
  await expect(secao).not.toContainText('Fontes da seção');
  await page.goto('/indicador.html?i=analfabetismo');
  await expect(page.locator('.competencias')).toContainText('CF art. 208, I');
  await page.goto('/indicador.html?i=mort_infantil');
  await expect(page.locator('.competencias')).toContainText('Lei nº 8.080/1990');
  await page.goto('/indicador.html?i=homicidios');
  await expect(page.locator('.competencias')).toContainText('CF art. 144');
  await page.goto('/indicador.html?i=esgoto');
  await expect(page.locator('.competencias')).toContainText('Lei nº 11.445/2007');
  await page.goto('/indicador.html?i=informalidade');
  await expect(page.locator('.competencias')).toContainText('LOAS');
  await page.goto('/indicador.html?i=pib_pc');
  await expect(page.locator('.competencias')).toContainText('CF art. 170');
  // O IDHM remete às áreas das suas dimensões.
  await page.goto('/indicador.html?i=idhm');
  await page.locator('.competencias a', { hasText: 'Esperança de vida' }).click();
  // O link leva ao mapa do indicador com a gaveta "Sobre" já aberta.
  await expect(page).toHaveURL(/i=esperanca_vida.*sobre=1/);
  await expect(page.locator('body')).toHaveAttribute('data-pronto', 'true');
  await expect(page.locator('#sobre-indicador')).toBeVisible();
  await expect(page.locator('#sobre-indicador .competencias')).toContainText('Lei nº 8.080/1990');
  await page.keyboard.press('Escape');
  await expect(page).not.toHaveURL(/sobre=1/);
});

test('valor do Brasil no ano e série do Brasil no painel', async ({ page }) => {
  await abrir(page, '?i=idhm&a=2024');
  const botao = page.locator('#valor-br');
  await expect(botao).toContainText('Brasil em 2024');
  await expect(botao).toContainText('0,805');
  await botao.click();
  await expect(page).toHaveURL(/uf=BR/);
  const painel = page.locator('#painel');
  await expect(painel.locator('.painel-titulo')).toHaveText('Brasil');
  await expect(painel.locator('.painel-valores')).toContainText('Brasil em 2024');
  await expect(painel.locator('.grafico svg')).toBeVisible();
  await expect(page.locator('#sel-uf')).toHaveValue('BR');
});

test('mapa e slider cabem na tela, e a roda do mouse rola a página', async ({ page }) => {
  await abrir(page, '?i=idhm');
  const altura = page.viewportSize()?.height ?? 0;
  const slider = await page.locator('#slider').boundingBox();
  expect((slider?.y ?? 0) + (slider?.height ?? 0)).toBeLessThanOrEqual(altura);
  const mapa = await page.locator('#mapa').boundingBox();
  expect(mapa?.height ?? 0).toBeGreaterThan(200);
  await page.mouse.move((mapa?.x ?? 0) + 100, (mapa?.y ?? 0) + 100);
  await page.mouse.wheel(0, 300);
  await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThan(0);
});
