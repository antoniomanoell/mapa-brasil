// Consultas puras sobre um indicador: segmentos, anos e valores. Sem DOM.

import type { Indicador, Ponto, Segmento } from './types';

/** Segmentos do subindicador. Séries de referência (papel "referencia") só entram se pedidas:
 * elas aparecem no painel da UF, nunca no mapa, no ranking ou no slider. */
export function segmentosDe(ind: Indicador, sub: string, comReferencia = false): Segmento[] {
  return ind.segmentos.filter(
    (s) => s.subindicador === sub && (comReferencia || (s.papel ?? 'principal') === 'principal'),
  );
}

/** Intervalo do slider: do primeiro ao último ano com dado em algum segmento (a partir de 2000). */
export function intervaloAnos(ind: Indicador, sub: string): [number, number] {
  const anos = segmentosDe(ind, sub).flatMap((s) => s.anos);
  return [Math.max(2000, Math.min(...anos)), Math.max(...anos)];
}

/** Segmentos que publicam o ano. Dois ou mais = sobreposição de metodologias (ex.: PNAD e PNADC). */
export function segmentosNoAno(ind: Indicador, sub: string, ano: number): Segmento[] {
  return segmentosDe(ind, sub).filter((s) => s.anos.includes(ano));
}

/** Segmento exibido no mapa: o pedido, se vale no ano; senão o mais recente (último a começar). */
export function segmentoVigente(
  ind: Indicador,
  sub: string,
  ano: number,
  pedido?: string,
): Segmento | undefined {
  const candidatos = segmentosNoAno(ind, sub, ano);
  return (
    candidatos.find((s) => s.id === pedido) ??
    [...candidatos].sort((a, b) => (a.anos[0] ?? 0) - (b.anos[0] ?? 0)).at(-1)
  );
}

/** Área de onde vem o valor da UF (ex.: "RM de Belém"), quando o indicador não é medido na UF
 * inteira. */
export function areaDe(seg: Segmento | undefined, codigo: string): string | undefined {
  return seg?.areas?.[codigo];
}

export function ponto(seg: Segmento | undefined, geo: string, ano: number): Ponto | undefined {
  return seg?.valores[geo]?.[String(ano)];
}

/** Classe de cor (0..n) de um valor dados os limites fixos da escala. */
export function classe(v: number, limites: number[]): number {
  let i = 0;
  while (i < limites.length && v > (limites[i] as number)) i++;
  return i;
}
