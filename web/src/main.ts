import { formatarNumero } from './format';

const app = document.querySelector<HTMLElement>('#app');
if (app) {
  app.textContent = `Indicadores BR — em construção (${formatarNumero(0.5, 1)})`;
}
