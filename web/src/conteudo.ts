// Textos em Markdown (web/src/content) para as páginas de conteúdo. Carregados sob demanda.

import { marked } from 'marked';

const textos = import.meta.glob<string>('./content/*.md', { query: '?raw', import: 'default' });

export const MARCA_REVISAO = '<!-- REVISAR -->';

export interface Texto {
  html: string;
  rascunho: boolean;
}

export async function carregarTexto(nome: string): Promise<Texto | undefined> {
  const carregar = textos[`./content/${nome}.md`];
  if (!carregar) return undefined;
  const md = await carregar();
  // Textos são do próprio projeto (revisados pelo mantenedor), não entrada de usuário.
  return {
    html: await marked.parse(md.replaceAll(MARCA_REVISAO, '')),
    rascunho: md.includes(MARCA_REVISAO),
  };
}

export const AVISO_RASCUNHO =
  '<p class="aviso-rascunho" role="note">Rascunho: este texto ainda não foi revisado pelo mantenedor.</p>';
