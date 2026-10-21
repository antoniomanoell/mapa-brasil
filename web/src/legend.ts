import { CORES, CSS_HACHURA } from './cores';
import { formatarNumero } from './format';
import type { Indicador } from './types';

/** Legenda com os limites fixos da escala, a direção e o "sem dado". */
export function renderLegenda(el: HTMLElement, ind: Indicador, sub: string): void {
  const lim = ind.escalas[sub]?.limites ?? [];
  const f = (x: number) => formatarNumero(x, ind.casas_decimais);
  const rotulos = CORES.map((_, i) => {
    if (i === 0) return `até ${f(lim[0] as number)}`;
    if (i === CORES.length - 1) return `acima de ${f(lim[i - 1] as number)}`;
    return `${f(lim[i - 1] as number)} a ${f(lim[i] as number)}`;
  });
  el.replaceChildren();
  const titulo = document.createElement('p');
  titulo.className = 'legenda-titulo';
  titulo.textContent = `${ind.unidade_detalhe} · mais escuro = maior`;
  const lista = document.createElement('ul');
  CORES.forEach((cor, i) => lista.append(item(cor, rotulos[i] as string)));
  lista.append(item(CSS_HACHURA, 'sem dado'));
  el.append(titulo, lista);
}

function item(fundo: string, texto: string): HTMLLIElement {
  const li = document.createElement('li');
  const amostra = document.createElement('span');
  amostra.className = 'amostra';
  amostra.style.background = fundo;
  amostra.setAttribute('aria-hidden', 'true');
  li.append(amostra, texto);
  return li;
}
