import { describe, expect, it } from 'vitest';
import { classe, intervaloAnos, segmentoVigente, segmentosNoAno } from '../src/series';
import { formatarValor } from '../src/format';
import { IND } from './fixtures';

describe('segmentos', () => {
  it('intervalo vai do primeiro ao último ano com dado', () => {
    expect(intervaloAnos(IND, 'geral')).toEqual([2001, 2025]);
  });

  it('sobreposição mostra os dois segmentos', () => {
    expect(segmentosNoAno(IND, 'geral', 2014).map((s) => s.id)).toEqual(['pnad', 'pnadc']);
  });

  it('ano de Censo é lacuna da PNAD', () => {
    expect(segmentosNoAno(IND, 'geral', 2010)).toEqual([]);
  });

  it('padrão é o segmento mais recente; respeita o pedido', () => {
    expect(segmentoVigente(IND, 'geral', 2014)?.id).toBe('pnadc');
    expect(segmentoVigente(IND, 'geral', 2014, 'pnad')?.id).toBe('pnad');
    expect(segmentoVigente(IND, 'geral', 2005, 'pnadc')?.id).toBe('pnad');
  });
});

describe('classe', () => {
  it('limites são inclusivos à esquerda da classe seguinte', () => {
    const lim = [10, 20, 30, 40];
    expect([5, 10, 10.1, 20, 35, 40, 99].map((v) => classe(v, lim))).toEqual([0, 0, 1, 1, 3, 3, 4]);
  });
});

describe('formatarValor', () => {
  it('usa a unidade do indicador', () => {
    expect(formatarValor(IND, 1234.4)).toBe('R$ 1.234');
    expect(formatarValor(IND, null)).toBe('sem dado');
    expect(formatarValor({ ...IND, unidade: 'por 100 mil hab.', casas_decimais: 1 }, 20.03)).toBe(
      '20,0 por 100 mil hab.',
    );
  });
});
