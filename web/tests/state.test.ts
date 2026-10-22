import { describe, expect, it, vi } from 'vitest';
import { Store, escreverUrl, indicadorPedido, lerUrl, normalizar } from '../src/state';
import { CAT, IND } from './fixtures';

describe('URL', () => {
  it('lê e restaura exatamente a tela', () => {
    const e = normalizar(lerUrl('?i=teste&s=geral&a=2014&g=pnad&uf=se&v=ranking'), IND);
    expect(e).toEqual({
      indicador: 'teste',
      sub: 'geral',
      ano: 2014,
      segmento: 'pnad',
      uf: 'SE',
      visao: 'ranking',
      sobre: false,
    });
    expect(escreverUrl(e, IND)).toBe('?i=teste&s=geral&a=2014&g=pnad&uf=SE&v=ranking');
  });

  it('parâmetros inválidos caem para os padrões', () => {
    const e = normalizar(lerUrl('?i=teste&s=xyz&a=1850&g=nada&uf=ZZ&v=pizza'), IND);
    expect(e).toEqual({
      indicador: 'teste',
      sub: 'geral',
      ano: 2025,
      segmento: undefined,
      uf: undefined,
      visao: 'mapa',
      sobre: false,
    });
  });

  it('guarda a gaveta "Sobre" aberta na URL (sobre=1)', () => {
    const e = normalizar(lerUrl('?a=2014&sobre=1'), IND);
    expect(e.sobre).toBe(true);
    expect(escreverUrl(e, IND)).toContain('sobre=1');
    expect(escreverUrl({ ...e, sobre: false }, IND)).not.toContain('sobre');
  });

  it('aceita o Brasil (uf=BR) como local escolhido', () => {
    const e = normalizar(lerUrl('?a=2014&uf=br'), IND);
    expect(e.uf).toBe('BR');
    expect(escreverUrl(e, IND)).toContain('uf=BR');
  });

  it('segmento que não vale no ano é descartado', () => {
    expect(normalizar(lerUrl('?a=2020&g=pnad'), IND).segmento).toBeUndefined();
  });

  it('ano não inteiro cai para o mais recente', () => {
    expect(normalizar(lerUrl('?a=2014.5'), IND).ano).toBe(2025);
  });

  it('indicador desconhecido cai para o primeiro do catálogo', () => {
    expect(indicadorPedido(lerUrl('?i=nao_existe'), CAT)).toBe('teste');
    expect(indicadorPedido(lerUrl('?i=outro'), CAT)).toBe('outro');
  });

  it('subindicador outro restringe o intervalo de anos', () => {
    expect(normalizar(lerUrl('?s=outro&a=2005'), IND).ano).toBe(2005);
    expect(normalizar(lerUrl('?s=outro&a=2015'), IND).ano).toBe(2010);
  });
});

describe('Store', () => {
  it('notifica com o estado anterior', () => {
    const s = new Store();
    const f = vi.fn();
    s.assinar(f);
    const e = normalizar({}, IND);
    s.definir(e);
    s.atualizar({ ano: 2014 });
    expect(f).toHaveBeenLastCalledWith({ ...e, ano: 2014 }, e);
  });
});
