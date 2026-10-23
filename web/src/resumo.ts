// Cartões-resumo do ano: Brasil (com a variação desde o ano anterior da mesma série), maior e
// menor valor entre os estados e a diferença entre eles. Só descrevem: "maior/menor", nunca
// "melhor/pior" (PROJECT.md, princípio 6).

import { ajuda } from './ajuda';
import { esc, formatarNumero, formatarValor, formatarValorCurto, unidadeSeparada } from './format';
import { areaDe, ponto } from './series';
import type { Indicador, Segmento } from './types';
import { BR, UFS, type UF } from './ufs';

export interface Resumo {
  br: number | undefined;
  variacao: { de: number; delta: number } | undefined;
  maior: { uf: UF; v: number } | undefined;
  menor: { uf: UF; v: number } | undefined;
  comDado: number;
}

/** Números dos cartões. A variação só compara anos da mesma série (segmento), nunca emenda. */
export function calcularResumo(seg: Segmento | undefined, ano: number): Resumo {
  const br = ponto(seg, BR, ano)?.v ?? undefined;
  const anterior = seg?.anos.filter((a) => a < ano).at(-1);
  const brAnterior = anterior !== undefined ? ponto(seg, BR, anterior)?.v : undefined;
  const variacao =
    typeof br === 'number' && typeof brAnterior === 'number' && anterior !== undefined
      ? { de: anterior, delta: br - brAnterior }
      : undefined;
  const valores = UFS.flatMap((uf) => {
    const v = ponto(seg, uf.codigo, ano)?.v;
    return typeof v === 'number' ? [{ uf, v }] : [];
  }).sort((a, b) => b.v - a.v);
  return {
    br: typeof br === 'number' ? br : undefined,
    variacao,
    maior: valores[0],
    menor: valores.at(-1),
    comDado: valores.length,
  };
}

/** Variação com unidade: "+R$ 146", "−1,2 p.p." (pontos percentuais), "+0,012". */
function sinal(ind: Indicador, delta: number): string {
  const casas = ind.casas_decimais;
  if (Number(Math.abs(delta).toFixed(casas)) === 0) return 'sem variação';
  const abs = Math.abs(delta);
  const txt = ind.unidade === '%' ? `${formatarNumero(abs, casas)} p.p.` : formatarValor(ind, abs);
  return `${delta > 0 ? '+' : '−'}${txt}`;
}

export function renderResumo(
  el: HTMLElement,
  ind: Indicador,
  seg: Segmento | undefined,
  ano: number,
  ufSelecionada: string | undefined,
  aoSelecionar: (sigla: string) => void,
): void {
  const r = calcularResumo(seg, ano);
  const unidade = unidadeSeparada(ind);
  // Número em destaque e a unidade, quando separada, em letra menor.
  const valorCartao = (v: number | undefined) =>
    `${esc(formatarValorCurto(ind, v))}${unidade && v !== undefined ? ` <span class="cartao-unidade">${esc(unidade)}</span>` : ''}`;
  const variacao = r.variacao
    ? `${sinal(ind, r.variacao.delta)} desde ${r.variacao.de}`
    : 'sem ano anterior na mesma série';
  const cartaoUf = (titulo: string, item: Resumo['maior']) =>
    item
      ? `<button type="button" class="cartao" data-uf="${esc(item.uf.sigla)}" aria-pressed="${item.uf.sigla === ufSelecionada}">
          <span class="cartao-rotulo">${titulo}</span>
          <span class="cartao-valor">${valorCartao(item.v)}</span>
          <span class="cartao-detalhe">${esc(item.uf.nome)}${areaDe(seg, item.uf.codigo) ? ` · ${esc(areaDe(seg, item.uf.codigo) as string)}` : ''}</span>
        </button>`
      : `<div class="cartao"><span class="cartao-rotulo">${titulo}</span><span class="cartao-valor">—</span></div>`;
  const diferenca =
    r.maior && r.menor ? formatarNumero(r.maior.v - r.menor.v, ind.casas_decimais) : '—';
  el.innerHTML = `
    <button type="button" class="cartao cartao-br" id="valor-br" data-uf="${BR}" aria-pressed="${ufSelecionada === BR}" title="Ver a série do Brasil">
      <span class="cartao-rotulo">Brasil em ${ano}</span>
      <span class="cartao-valor">${valorCartao(r.br)}</span>
      <span class="cartao-detalhe">${esc(variacao)}</span>
    </button>
    ${cartaoUf('Maior valor', r.maior)}
    ${cartaoUf('Menor valor', r.menor)}
    <div class="cartao cartao-com-ajuda">
      ${ajuda('ajuda-resumo', 'Como ler os cartões', '<strong>Brasil:</strong> valor do país no ano. A variação compara com o ano anterior da mesma série; pesquisas diferentes não se comparam. <strong>Maior e menor valor:</strong> entre os 27 estados; maior não quer dizer melhor, depende do indicador. <strong>Diferença:</strong> maior menos menor valor.')}
      <span class="cartao-rotulo">Diferença entre eles</span>
      <span class="cartao-valor">${esc(diferenca)}</span>
      <span class="cartao-detalhe">${r.comDado} de ${UFS.length} estados com dado</span>
    </div>`;
  for (const b of el.querySelectorAll<HTMLButtonElement>('button[data-uf]')) {
    const sigla = b.dataset['uf'] as string;
    b.addEventListener('click', () => aoSelecionar(sigla));
  }
}
