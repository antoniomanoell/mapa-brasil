// Páginas de conteúdo: "Sobre o indicador" (?i=<id>), Metodologia e Sobre.

import './style.css';
import { AVISO_RASCUNHO, carregarCompetencias, carregarTexto, secaoCompetencias } from './conteudo';
import { carregarCatalogo, carregarIndicador } from './data';
import { esc } from './format';
import { fichaTecnica } from './ficha';
import { iniciarTema } from './tema';

const $ = (sel: string) => document.querySelector(sel) as HTMLElement;

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
  const [ind, texto, competencias] = await Promise.all([
    carregarIndicador(cat, id),
    carregarTexto(id),
    carregarCompetencias(id),
  ]);
  document.title = `Sobre o indicador: ${ind.nome} — Indicadores BR`;
  document
    .querySelector('meta[name="description"]')
    ?.setAttribute('content', `O que mede, como ler, fontes e limitações: ${ind.nome}.`);
  alvo.innerHTML = `
    <p class="voltar"><a href="./?i=${esc(id)}">← Ver no mapa</a></p>
    <h1>${esc(ind.nome)}</h1>
    ${texto?.rascunho ? AVISO_RASCUNHO : ''}
    ${texto?.html ?? '<p>Texto em preparação.</p>'}
    ${secaoCompetencias(competencias)}
    ${fichaTecnica(ind)}`;
}

async function paginaTexto(alvo: HTMLElement, nome: string): Promise<void> {
  const texto = await carregarTexto(nome);
  alvo.innerHTML = `${texto?.rascunho ? AVISO_RASCUNHO : ''}${texto?.html ?? ''}`;
  const h1 = alvo.querySelector('h1');
  if (h1) document.title = `${h1.textContent} — Indicadores BR`;
}

iniciarTema();
const alvo = $('#conteudo');
const pagina = document.body.dataset['pagina'] ?? '';
(pagina === 'indicador' ? paginaIndicador(alvo) : paginaTexto(alvo, pagina))
  .then(() => (document.body.dataset['pronto'] = 'true'))
  .catch((erro: unknown) => {
    console.error(erro);
    alvo.innerHTML = '<p>Não foi possível carregar esta página.</p>';
  });
