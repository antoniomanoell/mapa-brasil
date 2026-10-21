// Carrega os arquivos de data/public/ (servidos na raiz do site). Indicadores sob demanda, com cache.

import type { Catalogo, Indicador } from './types';

const base = import.meta.env.BASE_URL;
const indicadores = new Map<string, Promise<Indicador>>();

async function json<T>(caminho: string): Promise<T> {
  const resp = await fetch(`${base}${caminho}`);
  if (!resp.ok) throw new Error(`falha ao carregar ${caminho}: ${resp.status}`);
  return (await resp.json()) as T;
}

export const carregarCatalogo = (): Promise<Catalogo> => json<Catalogo>('catalog.json');

export const carregarMalha = (): Promise<unknown> => json<unknown>('geo/uf.topojson');

export function carregarIndicador(cat: Catalogo, id: string): Promise<Indicador> {
  let p = indicadores.get(id);
  if (!p) {
    const item = cat.indicadores.find((i) => i.id === id);
    if (!item) throw new Error(`indicador desconhecido: ${id}`);
    p = json<Indicador>(item.arquivo);
    indicadores.set(id, p);
  }
  return p;
}
