// Testes de fumaça (PROJECT.md, 5.1): carregar, trocar indicador, mover slider, clicar UF.

import { type Page, expect, test } from '@playwright/test';

async function abrir(page: Page, query = '') {
  await page.goto(`/${query}`);
  await expect(page.locator('body')).toHaveAttribute('data-pronto', 'true', { timeout: 20_000 });
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
