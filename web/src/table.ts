// Ranking do ano: alternativa acessível ao mapa e contrapeso ao viés de área (PROJECT.md, 3).

import { ROTULO_FLAG, esc, formatarValor, formatarValorCurto, unidadeSeparada } from './format';
import { ponto } from './series';
import type { Indicador, Segmento } from './types';
import { BR, UFS } from './ufs';

export function renderRanking(
  el: HTMLElement,
  ind: Indicador,
  seg: Segmento | undefined,
  ano: number,
  ufSelecionada: string | undefined,
  aoSelecionar: (sigla: string) => void,
): void {
  el.replaceChildren();
  const linhas = UFS.map((uf) => ({ uf, p: ponto(seg, uf.codigo, ano) }));
  const comValor = linhas
    .filter((l) => typeof l.p?.v === 'number')
    .sort((a, b) => (b.p?.v as number) - (a.p?.v as number));
  const semValor = linhas.filter((l) => typeof l.p?.v !== 'number');
  const br = ponto(seg, BR, ano)?.v;
  const max = Math.max(...comValor.map((l) => l.p?.v as number), br ?? 0) || 1;

  const tabela = document.createElement('table');
  tabela.className = 'ranking';
  // A legenda completa fica para leitores de tela; o painel mostra um título curto.
  tabela.innerHTML = `
    <caption class="so-leitor">${esc(ind.nome)} — ${ano}${seg ? ` · ${esc(seg.rotulo)}` : ''} · do maior para o menor</caption>
    <thead><tr><th scope="col">#</th><th scope="col">Estado</th><th scope="col">Valor${unidadeSeparada(ind) ? ` <span class="th-unidade">(${esc(unidadeSeparada(ind))})</span>` : ''}</th></tr></thead>`;
  const corpo = document.createElement('tbody');

  const pctBr = typeof br === 'number' ? (br / max) * 100 : undefined;
  comValor.forEach(({ uf, p }, i) => {
    const tr = document.createElement('tr');
    if (uf.sigla === ufSelecionada) tr.className = 'selecionada';
    const flags = (p?.flags ?? []).map((f) => ROTULO_FLAG[f]).join('; ');
    const pct = ((p?.v as number) / max) * 100;
    tr.innerHTML = `
      <td class="pos">${i + 1}</td>
      <td><button type="button" class="link-uf"></button></td>
      <td class="valor"><span class="valor-linha">
        <span class="barra-trilho">
          <span class="barra" style="width:${pct}%"></span>
          ${pctBr !== undefined ? `<span class="ref-br" style="left:${pctBr}%" title="Brasil"></span>` : ''}
        </span>
        <span class="num">${formatarValorCurto(ind, p?.v)}${flags ? ' *' : ''}</span>
      </span></td>`;
    const botao = tr.querySelector('button') as HTMLButtonElement;
    botao.textContent = uf.nome;
    botao.addEventListener('click', () => aoSelecionar(uf.sigla));
    if (flags) (tr.querySelector('.num') as HTMLElement).title = flags;
    corpo.append(tr);
  });
  for (const { uf } of semValor) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td class="pos">—</td><td></td><td class="valor sem-dado">sem dado</td>`;
    (tr.children[1] as HTMLElement).textContent = uf.nome;
    corpo.append(tr);
  }
  tabela.append(corpo);

  const cabeca = document.createElement('div');
  cabeca.className = 'bloco-cabeca';
  cabeca.innerHTML = `<h2 class="bloco-titulo">Estados, do maior para o menor</h2>
    <p class="bloco-dica"></p>`;
  (cabeca.lastElementChild as HTMLElement).textContent =
    `Brasil: ${formatarValor(ind, br)} (linha cinza nas barras)`;
  // Só a lista rola; o título do painel fica parado.
  const rolagem = document.createElement('div');
  rolagem.className = 'ranking-rolagem';
  rolagem.append(tabela);
  el.append(cabeca, rolagem);
}
