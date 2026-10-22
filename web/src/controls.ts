// Seletor de indicador agrupado por tema, recorte (botões quando são poucos) e escolha de estado.

// Até este número de recortes, eles viram botões junto do mapa; acima, um seletor no cabeçalho.
const MAX_BOTOES_RECORTE = 4;

import type { Catalogo, Indicador } from './types';
import { UFS } from './ufs';

export interface Controles {
  atualizar(cat: Catalogo, ind: Indicador, sub: string, uf: string | undefined): void;
}

export function criarControles(
  el: HTMLElement,
  aoIndicador: (id: string) => void,
  aoSub: (sub: string) => void,
  aoUf: (sigla: string | undefined) => void,
): Controles {
  // O index.html já traz esta marcação (evita deslocar a página ao carregar); recria só se faltar.
  if (!el.querySelector('#sel-indicador')) {
    el.innerHTML = `
    <label class="campo">Indicador <select id="sel-indicador"></select></label>
    <label class="campo" id="campo-sub">Recorte <select id="sel-sub"></select></label>
    <label class="campo">Estado <select id="sel-uf"><option value="">— nenhum —</option></select></label>`;
  }
  const selInd = el.querySelector('#sel-indicador') as HTMLSelectElement;
  const selSub = el.querySelector('#sel-sub') as HTMLSelectElement;
  const campoSub = el.querySelector('#campo-sub') as HTMLElement;
  const selUf = el.querySelector('#sel-uf') as HTMLSelectElement;
  const recortes = document.querySelector('#recortes') as HTMLElement | null;
  selUf.add(new Option('Brasil', 'BR'));
  for (const uf of [...UFS].sort((a, b) => a.nome.localeCompare(b.nome, 'pt-BR'))) {
    selUf.add(new Option(uf.nome, uf.sigla));
  }
  selInd.addEventListener('change', () => aoIndicador(selInd.value));
  selSub.addEventListener('change', () => aoSub(selSub.value));
  selUf.addEventListener('change', () => aoUf(selUf.value || undefined));

  let catalogoMontado: Catalogo | undefined;
  return {
    atualizar(cat, ind, sub, uf) {
      if (catalogoMontado !== cat) {
        selInd.replaceChildren();
        const temas = new Map<string, HTMLOptGroupElement>();
        for (const item of cat.indicadores) {
          let grupo = temas.get(item.tema);
          if (!grupo) {
            grupo = document.createElement('optgroup');
            grupo.label = item.tema;
            temas.set(item.tema, grupo);
          }
          grupo.append(new Option(item.nome, item.id));
        }
        [...temas.entries()]
          .sort(([a], [b]) => a.localeCompare(b, 'pt-BR'))
          .forEach(([, g]) => selInd.append(g));
        catalogoMontado = cat;
      }
      selInd.value = ind.id;
      selSub.replaceChildren(...ind.subindicadores.map((s) => new Option(s.nome, s.id)));
      selSub.value = sub;
      const n = ind.subindicadores.length;
      const emBotoes = recortes !== null && n >= 2 && n <= MAX_BOTOES_RECORTE;
      campoSub.hidden = n < 2 || emBotoes;
      if (recortes) {
        recortes.hidden = !emBotoes;
        recortes.replaceChildren(
          ...(emBotoes ? ind.subindicadores : []).map((s) => {
            const b = document.createElement('button');
            b.type = 'button';
            b.textContent = s.nome;
            b.setAttribute('aria-pressed', String(s.id === sub));
            b.addEventListener('click', () => aoSub(s.id));
            return b;
          }),
        );
      }
      selUf.value = uf ?? '';
    },
  };
}
