import type { Flag, Indicador } from './types';

const cache = new Map<number, Intl.NumberFormat>();

/** Formata um número em pt-BR (vírgula decimal, ponto de milhar) com casas fixas. */
export function formatarNumero(valor: number, casasDecimais: number): string {
  let fmt = cache.get(casasDecimais);
  if (!fmt) {
    fmt = new Intl.NumberFormat('pt-BR', {
      minimumFractionDigits: casasDecimais,
      maximumFractionDigits: casasDecimais,
    });
    cache.set(casasDecimais, fmt);
  }
  return fmt.format(valor);
}

/** Valor com a unidade do indicador: "R$ 1.234", "20,1 por 100 mil hab.", "0,805". */
export function formatarValor(ind: Indicador, v: number | null | undefined): string {
  if (v === null || v === undefined) return 'sem dado';
  const n = formatarNumero(v, ind.casas_decimais);
  if (ind.unidade === 'R$') return `R$ ${n}`;
  if (ind.unidade === '%') return `${n}%`;
  if (ind.unidade === 'índice') return n;
  return `${n} ${ind.unidade}`;
}

/** Escapa texto para interpolar em HTML. */
export function esc(texto: string): string {
  return texto.replace(
    /[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c] as string,
  );
}

export const ROTULO_FLAG: Record<Flag, string> = {
  baixa_precisao: 'baixa precisão (coeficiente de variação alto)',
  cobertura_urbana: 'cobertura apenas urbana — não comparável',
  estimativa: 'estimativa',
  preliminar: 'preliminar',
};
