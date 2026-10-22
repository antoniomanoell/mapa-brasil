// Ficha técnica de um indicador, gerada do JSON publicado. Usada na gaveta do mapa e na página.

import { esc } from './format';
import type { Indicador } from './types';

export function formatarData(iso: string): string {
  const [a, m, d] = iso.split('-');
  return `${d}/${m}/${a}`;
}

function faixas(anos: number[]): string {
  const partes: string[] = [];
  let ini = anos[0] as number;
  let fim = ini;
  for (const a of anos.slice(1)) {
    if (a === fim + 1) {
      fim = a;
      continue;
    }
    partes.push(fim > ini ? `${ini}–${fim}` : String(ini));
    ini = fim = a;
  }
  partes.push(fim > ini ? `${ini}–${fim}` : String(ini));
  return partes.join(', ');
}

/** Ficha técnica gerada do próprio JSON publicado: nunca fica desatualizada. */
export function fichaTecnica(ind: Indicador): string {
  const subs = new Map(ind.subindicadores.map((s) => [s.id, s.nome]));
  const segmentos = ind.segmentos
    .map(
      (s) => `
      <section class="ficha-segmento">
        <h3>${esc(s.rotulo)}${ind.subindicadores.length > 1 ? ` · ${esc(subs.get(s.subindicador) ?? '')}` : ''}${
          s.papel === 'referencia' ? ' <span class="selo">série de referência</span>' : ''
        }</h3>
        <dl>
          <dt>Fonte</dt><dd><a href="${esc(s.fonte_url)}" rel="noopener">${esc(s.fonte)}</a></dd>
          <dt>Tabela</dt><dd>${esc(s.tabela)}</dd>
          <dt>Anos</dt><dd>${esc(faixas(s.anos))}</dd>
          <dt>Extraído em</dt><dd>${esc(formatarData(s.extraido_em))}</dd>
          ${s.notas ? `<dt>Notas</dt><dd>${esc(s.notas)}</dd>` : ''}
        </dl>
      </section>`,
    )
    .join('');
  const quebras = (ind.quebras ?? [])
    .map((q) => `<li><strong>${q.ano}:</strong> ${esc(q.texto)}</li>`)
    .join('');
  return `
    <h2>Ficha técnica</h2>
    <p class="ficha-intro">Gerada automaticamente a partir dos dados publicados. ${esc(ind.unidade_detalhe)}.</p>
    ${segmentos}
    ${quebras ? `<h3>Quebras de série</h3><ul>${quebras}</ul>` : ''}
    <p class="ficha-versao">Versão do pipeline: <code>${esc(ind.versao_pipeline)}</code></p>`;
}
