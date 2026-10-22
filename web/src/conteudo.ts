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

// Seção "Quem é responsável": texto por área (content/competencias/<area>.md) mais o bloco comum
// sobre os Poderes. FONTES.md, da mesma pasta, é só registro interno e não é carregado.
const competencias = import.meta.glob<string>('./content/competencias/[a-z]*.md', {
  query: '?raw',
  import: 'default',
});

const FONTES = '### Fontes';

/** Área de competências de cada indicador; indicador sem área ainda não mostra a seção. */
export const AREA_COMPETENCIAS: Record<string, string> = {
  ideb: 'educacao',
  analfabetismo: 'educacao',
  mort_infantil: 'saude',
  esperanca_vida: 'saude',
};

export const AVISO_COMPETENCIAS =
  '<p class="aviso-competencias">Esta seção descreve as atribuições definidas em lei. Ela não avalia governos nem explica a variação do indicador.</p>';

export async function carregarCompetencias(indicador: string): Promise<Texto | undefined> {
  const area = AREA_COMPETENCIAS[indicador];
  const carregarArea = area ? competencias[`./content/competencias/${area}.md`] : undefined;
  const carregarPoderes = competencias['./content/competencias/poderes.md'];
  if (!carregarArea || !carregarPoderes) return undefined;
  const [md, poderes] = await Promise.all([carregarArea(), carregarPoderes()]);
  // Ordem: texto da área, bloco dos Poderes e, no fim, as fontes de ambos numa lista só.
  const [corpoArea, fontesArea = ''] = md.split(FONTES);
  const [corpoPoderes, fontesPoderes = ''] = poderes.split(FONTES);
  const junto = [corpoArea, corpoPoderes, FONTES, fontesArea.trim(), fontesPoderes.trim()].join(
    '\n',
  );
  return {
    html: await marked.parse(junto.replaceAll(MARCA_REVISAO, '')),
    rascunho: junto.includes(MARCA_REVISAO),
  };
}

/** HTML da seção completa, ou vazio se o indicador ainda não tem texto de competências. */
export function secaoCompetencias(texto: Texto | undefined): string {
  if (!texto) return '';
  return `<section class="competencias">
    <h2>Quem é responsável</h2>
    ${texto.rascunho ? AVISO_RASCUNHO : ''}
    ${AVISO_COMPETENCIAS}
    ${texto.html}
  </section>`;
}
