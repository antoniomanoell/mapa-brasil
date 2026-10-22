// Páginas de conteúdo: "Sobre o indicador" (?i=<id>), Metodologia e Sobre.

import './style.css';
import { AVISO_RASCUNHO, carregarTexto } from './conteudo';
import { carregarCatalogo, carregarIndicador } from './data';
import { esc } from './format';
import type { Indicador } from './types';

const $ = (sel: string) => document.querySelector(sel) as HTMLElement;

function formatarData(iso: string): string {
  const [a, m, d] = iso.split('-');
  return `${d}/${m}/${a}`;
}

function faixas(anos: number[]): string {
  const partes: string[] = [];
  let ini = anos[0] as number;
  let fim = ini;
  for (const a of anos.slice(1)) {
    if (a === fim + 1) {
      fim = a;
      continue;
    }
    partes.push(fim > ini ? `${ini}–${fim}` : String(ini));
    ini = fim = a;
  }
  partes.push(fim > ini ? `${ini}–${fim}` : String(ini));
  return partes.join(', ');
}

/** Ficha técnica gerada do próprio JSON publicado: nunca fica desatualizada. */
function fichaTecnica(ind: Indicador): string {
  const subs = new Map(ind.subindicadores.map((s) => [s.id, s.nome]));
  const segmentos = ind.segmentos
    .map(
      (s) => `
      <section class="ficha-segmento">
        <h3>${esc(s.rotulo)}${ind.subindicadores.length > 1 ? ` · ${esc(subs.get(s.subindicador) ?? '')}` : ''}${
          s.papel === 'referencia' ? ' <span class="selo">série de referência</span>' : ''
        }</h3>
        <dl>
          <dt>Fonte</dt><dd><a href="${esc(s.fonte_url)}" rel="noopener">${esc(s.fonte)}</a></dd>
          <dt>Tabela</dt><dd>${esc(s.tabela)}</dd>
          <dt>Anos</dt><dd>${esc(faixas(s.anos))}</dd>
          <dt>Extraído em</dt><dd>${esc(formatarData(s.extraido_em))}</dd>
          ${s.notas ? `<dt>Notas</dt><dd>${esc(s.notas)}</dd>` : ''}
        </dl>
      </section>`,
    )
    .join('');
  const quebras = (ind.quebras ?? [])
    .map((q) => `<li><strong>${q.ano}:</strong> ${esc(q.texto)}</li>`)
    .join('');
  return `
    <h2>Ficha técnica</h2>
    <p class="ficha-intro">Gerada automaticamente a partir dos dados publicados. ${esc(ind.unidade_detalhe)}.</p>
    ${segmentos}
    ${quebras ? `<h3>Quebras de série</h3><ul>${quebras}</ul>` : ''}
    <p class="ficha-versao">Versão do pipeline: <code>${esc(ind.versao_pipeline)}</code></p>`;
}

async function paginaIndicador(alvo: HTMLElement): Promise<void> {
  const cat = await carregarCatalogo();
  const id = new URLSearchParams(location.search).get('i') ?? '';
  const item = cat.indicadores.find((i) => i.id === id);
  if (!item) {
    alvo.innerHTML = `<h1>Indicador não encontrado</h1>
      <ul>${cat.indicadores
        .map((i) => `<li><a href="indicador.html?i=${esc(i.id)}">${esc(i.nome)}</a></li>`)
        .join('')}</ul>`;
    return;
  }
  const [ind, texto] = await Promise.all([carregarIndicador(cat, id), carregarTexto(id)]);
  document.title = `Sobre o indicador: ${ind.nome} — Indicadores BR`;
  document
    .querySelector('meta[name="description"]')
    ?.setAttribute('content', `O que mede, como ler, fontes e limitações: ${ind.nome}.`);
  alvo.innerHTML = `
    <p class="voltar"><a href="./?i=${esc(id)}">← Ver no mapa</a></p>
    <h1>${esc(ind.nome)}</h1>
    ${texto?.rascunho ? AVISO_RASCUNHO : ''}
    ${texto?.html ?? '<p>Texto em preparação.</p>'}
    ${fichaTecnica(ind)}`;
}

async function paginaTexto(alvo: HTMLElement, nome: string): Promise<void> {
  const texto = await carregarTexto(nome);
  alvo.innerHTML = `${texto?.rascunho ? AVISO_RASCUNHO : ''}${texto?.html ?? ''}`;
  const h1 = alvo.querySelector('h1');
  if (h1) document.title = `${h1.textContent} — Indicadores BR`;
}

const alvo = $('#conteudo');
const pagina = document.body.dataset['pagina'] ?? '';
(pagina === 'indicador' ? paginaIndicador(alvo) : paginaTexto(alvo, pagina))
  .then(() => (document.body.dataset['pronto'] = 'true'))
  .catch((erro: unknown) => {
    console.error(erro);
    alvo.innerHTML = '<p>Não foi possível carregar esta página.</p>';
  });
