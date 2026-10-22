// Gera public/og.png (1200×630) a partir de scripts/og.html. Rodar só quando o cartão mudar:
//   node scripts/gerar-og.mjs
import { chromium } from '@playwright/test';
import { fileURLToPath } from 'node:url';

const html = new URL('./og.html', import.meta.url);
const saida = fileURLToPath(new URL('../public/og.png', import.meta.url));

const navegador = await chromium.launch();
const pagina = await navegador.newPage({ viewport: { width: 1200, height: 630 } });
await pagina.goto(html.href);
await pagina.screenshot({ path: saida });
await navegador.close();
console.log(`gerado: ${saida}`);
