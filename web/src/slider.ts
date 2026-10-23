// Slider temporal com play/pause e escolha de segmento quando dois valem no mesmo ano (9.1).

import { intervaloAnos, segmentoVigente, segmentosNoAno } from './series';
import type { Indicador } from './types';

const PASSO_MS = 900;

export interface AoMudarAno {
  (ano: number): void;
}

const ICONE_PLAY =
  '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M4 2.5v11l9-5.5z" fill="currentColor"/></svg>';
const ICONE_PAUSA =
  '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M4 2.5h3v11H4zM9 2.5h3v11H9z" fill="currentColor"/></svg>';

export class Slider {
  #range: HTMLInputElement;
  #rotulo: HTMLElement;
  #play: HTMLButtonElement;
  #segmentos: HTMLElement;
  #timer: number | undefined;
  #fim = 0;
  #ini = 0;

  constructor(
    el: HTMLElement,
    private aoMudarAno: AoMudarAno,
    private aoMudarSegmento: (seg: string) => void,
  ) {
    el.innerHTML = `
      <div class="slider-linha">
        <button type="button" class="play" aria-label="Animar ao longo dos anos">${ICONE_PLAY}</button>
        <input type="range" step="1" aria-label="Ano">
        <output class="slider-rotulo" aria-live="polite"></output>
      </div>
      <fieldset class="segmentos" hidden>
        <legend>Duas pesquisas cobrem este ano. Ver no mapa:</legend>
      </fieldset>`;
    this.#range = el.querySelector('input') as HTMLInputElement;
    this.#rotulo = el.querySelector('output') as HTMLElement;
    this.#play = el.querySelector('.play') as HTMLButtonElement;
    this.#segmentos = el.querySelector('.segmentos') as HTMLElement;
    this.#range.addEventListener('input', () => {
      this.parar();
      this.#pintar();
      this.aoMudarAno(Number(this.#range.value));
    });
    this.#play.addEventListener('click', () => (this.#timer ? this.parar() : this.#tocar()));
  }

  atualizar(ind: Indicador, sub: string, ano: number, pedido: string | undefined): void {
    const [ini, fim] = intervaloAnos(ind, sub);
    this.#ini = ini;
    this.#fim = fim;
    this.#range.min = String(ini);
    this.#range.max = String(fim);
    this.#range.value = String(ano);
    this.#pintar();
    const vigente = segmentoVigente(ind, sub, ano, pedido);
    this.#rotulo.textContent = vigente ? `${ano} · ${vigente.rotulo}` : `${ano} · sem dado`;
    this.#range.setAttribute('aria-valuetext', this.#rotulo.textContent);

    const candidatos = segmentosNoAno(ind, sub, ano);
    this.#segmentos.hidden = candidatos.length < 2;
    this.#segmentos.querySelectorAll('label').forEach((l) => l.remove());
    if (candidatos.length >= 2) {
      for (const s of candidatos) {
        const label = document.createElement('label');
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'segmento';
        radio.value = s.id;
        radio.checked = s.id === vigente?.id;
        radio.addEventListener('change', () => this.aoMudarSegmento(s.id));
        label.append(radio, ` ${s.rotulo}`);
        this.#segmentos.append(label);
      }
    }
  }

  parar(): void {
    if (this.#timer) window.clearInterval(this.#timer);
    this.#timer = undefined;
    this.#play.innerHTML = ICONE_PLAY;
    this.#play.setAttribute('aria-label', 'Animar ao longo dos anos');
  }

  /** Trilho preenchido até o ano escolhido (o CSS lê --progresso). */
  #pintar(): void {
    const total = this.#fim - this.#ini;
    const pct = total > 0 ? ((Number(this.#range.value) - this.#ini) / total) * 100 : 100;
    this.#range.style.setProperty('--progresso', `${pct}%`);
  }

  #tocar(): void {
    if (Number(this.#range.value) >= this.#fim) this.aoMudarAno(this.#ini);
    this.#play.innerHTML = ICONE_PAUSA;
    this.#play.setAttribute('aria-label', 'Pausar animação');
    this.#timer = window.setInterval(() => {
      const prox = Number(this.#range.value) + 1;
      if (prox > this.#fim) return this.parar();
      this.aoMudarAno(prox);
    }, PASSO_MS);
  }
}
