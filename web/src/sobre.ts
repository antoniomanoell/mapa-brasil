// Gaveta "Sobre este indicador" na própria página do mapa: texto revisado e ficha técnica.

import { AVISO_RASCUNHO, carregarTexto } from './conteudo';
import { fichaTecnica } from './ficha';
import { esc } from './format';
import type { Indicador } from './types';

export class SobreIndicador {
  #el: HTMLElement;
  #corpo: HTMLElement;
  #titulo: HTMLElement;
  #origem: HTMLElement | null = null;
  #pedido = 0;

  constructor(el: HTMLElement) {
    this.#el = el;
    el.innerHTML = `
      <div class="painel-cabeca">
        <h2 class="painel-titulo" id="sobre-titulo" tabindex="-1"></h2>
        <button type="button" class="fechar" aria-label="Fechar informações do indicador">✕</button>
      </div>
      <div class="texto-gaveta"></div>`;
    this.#titulo = el.querySelector('.painel-titulo') as HTMLElement;
    this.#corpo = el.querySelector('.texto-gaveta') as HTMLElement;
    (el.querySelector('.fechar') as HTMLButtonElement).addEventListener('click', () =>
      this.fechar(),
    );
    // Na fase de captura, para o Esc fechar só esta gaveta, e não também o painel do estado.
    document.addEventListener(
      'keydown',
      (e) => {
        if (e.key === 'Escape' && !el.hidden) {
          e.stopImmediatePropagation();
          this.fechar();
        }
      },
      true,
    );
  }

  get aberta(): boolean {
    return !this.#el.hidden;
  }

  async abrir(ind: Indicador, origem?: HTMLElement | null): Promise<void> {
    const pedido = ++this.#pedido;
    if (origem) this.#origem = origem;
    this.#titulo.textContent = ind.nome;
    if (this.#el.hidden) {
      this.#corpo.innerHTML = '<p>Carregando…</p>';
      this.#el.hidden = false;
      this.#titulo.focus();
    }
    const texto = await carregarTexto(ind.id);
    if (pedido !== this.#pedido) return; // trocou de indicador no meio do carregamento
    this.#corpo.innerHTML = `
      ${texto?.rascunho ? AVISO_RASCUNHO : ''}
      ${texto?.html ?? '<p>Texto em preparação.</p>'}
      ${fichaTecnica(ind)}
      <p class="ficha-link"><a href="indicador.html?i=${esc(ind.id)}">Abrir em página própria</a></p>`;
    this.#el.scrollTop = 0;
  }

  fechar(): void {
    if (this.#el.hidden) return;
    this.#el.hidden = true;
    this.#origem?.focus();
    this.#origem = null;
  }
}
