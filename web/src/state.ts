// Estado da tela e sua sincronização com a URL (PROJECT.md, 9.3).
// ?i=<id>&s=<subindicador>&a=<ano>&g=<segmento>&uf=<sigla>&v=<mapa|ranking>&sobre=1

import { intervaloAnos, segmentosNoAno } from './series';
import type { Catalogo, Indicador } from './types';
import { localPorSigla } from './ufs';

export type Visao = 'mapa' | 'ranking';

export interface Estado {
  indicador: string;
  sub: string;
  ano: number;
  segmento?: string;
  uf?: string; // sigla da UF, ou "BR" para o Brasil
  visao: Visao;
  sobre: boolean; // gaveta "Sobre este indicador" aberta
}

export interface EstadoBruto {
  i?: string;
  s?: string;
  a?: string;
  g?: string;
  uf?: string;
  v?: string;
  sobre?: string;
}

export function lerUrl(search: string): EstadoBruto {
  const p = new URLSearchParams(search);
  const bruto: EstadoBruto = {};
  for (const k of ['i', 's', 'a', 'g', 'uf', 'v', 'sobre'] as const) {
    const valor = p.get(k);
    if (valor) bruto[k] = valor;
  }
  return bruto;
}

/** Indicador pedido na URL, ou o primeiro do catálogo. */
export function indicadorPedido(bruto: EstadoBruto, cat: Catalogo): string {
  const ids = cat.indicadores.map((i) => i.id);
  return bruto.i && ids.includes(bruto.i) ? bruto.i : (ids[0] as string);
}

/** Completa e corrige o estado: parâmetro inválido cai para o padrão, sem quebrar. */
export function normalizar(bruto: EstadoBruto, ind: Indicador): Estado {
  const subs = ind.subindicadores.map((s) => s.id);
  const sub = bruto.s && subs.includes(bruto.s) ? bruto.s : (subs[0] as string);
  const [ini, fim] = intervaloAnos(ind, sub);
  const anoPedido = Number(bruto.a);
  const ano = Number.isInteger(anoPedido) && anoPedido >= ini && anoPedido <= fim ? anoPedido : fim;
  const segs = segmentosNoAno(ind, sub, ano).map((s) => s.id);
  const segmento = bruto.g && segs.includes(bruto.g) ? bruto.g : undefined;
  const uf = bruto.uf ? localPorSigla(bruto.uf)?.sigla : undefined;
  const visao: Visao = bruto.v === 'ranking' ? 'ranking' : 'mapa';
  return { indicador: ind.id, sub, ano, segmento, uf, visao, sobre: bruto.sobre === '1' };
}

export function escreverUrl(e: Estado, ind: Indicador): string {
  const p = new URLSearchParams();
  p.set('i', e.indicador);
  if (ind.subindicadores.length > 1) p.set('s', e.sub);
  p.set('a', String(e.ano));
  if (e.segmento) p.set('g', e.segmento);
  if (e.uf) p.set('uf', e.uf);
  if (e.visao !== 'mapa') p.set('v', e.visao);
  if (e.sobre) p.set('sobre', '1');
  return `?${p.toString()}`;
}

type Ouvinte = (e: Estado, anterior: Estado | undefined) => void;

/** Store mínimo: um estado, assinantes notificados a cada mudança. */
export class Store {
  #estado: Estado | undefined;
  #ouvintes: Ouvinte[] = [];

  get estado(): Estado {
    if (!this.#estado) throw new Error('estado ainda não inicializado');
    return this.#estado;
  }

  assinar(f: Ouvinte): void {
    this.#ouvintes.push(f);
  }

  definir(novo: Estado): void {
    const anterior = this.#estado;
    this.#estado = novo;
    for (const f of this.#ouvintes) f(novo, anterior);
  }

  atualizar(parcial: Partial<Estado>): void {
    this.definir({ ...this.estado, ...parcial });
  }
}
