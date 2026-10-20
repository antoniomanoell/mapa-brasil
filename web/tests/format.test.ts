import { describe, expect, it } from 'vitest';
import { formatarNumero } from '../src/format';

describe('formatarNumero', () => {
  it('usa vírgula decimal e ponto de milhar', () => {
    expect(formatarNumero(1234.567, 1)).toBe('1.234,6');
  });

  it('respeita zero casas decimais', () => {
    expect(formatarNumero(801.2, 0)).toBe('801');
  });

  it('completa com zeros', () => {
    expect(formatarNumero(0.7, 3)).toBe('0,700');
  });
});
