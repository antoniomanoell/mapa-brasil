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
