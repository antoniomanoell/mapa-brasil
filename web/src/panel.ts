// Painel da UF: série temporal com segmentos separados, Brasil em cinza, quebras marcadas (9.1).
// Observable Plot só é baixado quando o painel abre pela primeira vez.

import { COR_BRASIL } from './cores';
import { ROTULO_FLAG, esc, formatarNumero, formatarValor } from './format';
import { ponto, segmentoVigente, segmentosDe } from './series';
import type { Indicador } from './types';
import { BR, ufPorSigla } from './ufs';

// Cores dos segmentos da UF: escuras, distintas entre si e do cinza do Brasil; sem vermelho/verde.
const CORES_SEGMENTO = ['#08519c', '#6a3d9a'];
// Série de referência (ex.: taxa direta do DATASUS): tracejada, só para a UF.
const COR_REFERENCIA = '#b15928';

interface Linha {
  ano: number;
  v: number | null;
  serie: string;
  rotulo: string;
  cor: string;
  marcado: boolean;
  detalhe: string;
  referencia: boolean;
  // Série com dado a cada dois anos (Ideb): os pontos são ligados só visualmente, tracejado.
  bienal: boolean;
}

export class Painel {
  #el: HTMLElement;
  #corpo: HTMLElement;
  #titulo: HTMLElement;

  constructor(el: HTMLElement, aoFechar: () => void) {
    this.#el = el;
    el.innerHTML = `
      <div class="painel-cabeca">
        <h2 class="painel-titulo" tabindex="-1"></h2>
        <button type="button" class="fechar" aria-label="Fechar painel do estado">✕</button>
      </div>
      <div class="painel-corpo"></div>`;
    this.#titulo = el.querySelector('.painel-titulo') as HTMLElement;
    this.#corpo = el.querySelector('.painel-corpo') as HTMLElement;
    (el.querySelector('.fechar') as HTMLButtonElement).addEventListener('click', aoFechar);
    // Esc fecha a gaveta de qualquer lugar da página, não só com o foco dentro dela.
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !el.hidden) aoFechar();
    });
  }

  fechar(): void {
    this.#el.hidden = true;
  }

  async abrir(
    ind: Indicador,
    sub: string,
    ano: number,
    pedido: string | undefined,
    sigla: string,
  ): Promise<void> {
    const uf = ufPorSigla(sigla);
    if (!uf) return this.fechar();
    const estavaFechado = this.#el.hidden;
    this.#el.hidden = false;
    const nomeSub = ind.subindicadores.find((s) => s.id === sub)?.nome ?? ind.nome;
    this.#titulo.textContent = uf.nome;

    const vigente = segmentoVigente(ind, sub, ano, pedido);
    const pUf = ponto(vigente, uf.codigo, ano);
    const pBr = ponto(vigente, BR, ano);
    const segs = segmentosDe(ind, sub, true);
    const linhas: Linha[] = [];
    let iPrincipal = 0;
    segs.forEach((seg) => {
      const referencia = seg.papel === 'referencia';
      const bienal =
        seg.anos.length > 2 &&
        seg.anos.every((a, i) => i === 0 || a - (seg.anos[i - 1] as number) === 2);
      const cor = referencia
        ? COR_REFERENCIA
        : (CORES_SEGMENTO[iPrincipal++ % CORES_SEGMENTO.length] as string);
      const series: [string, string, string][] = [[uf.codigo, `${uf.sigla} · ${seg.rotulo}`, cor]];
      if (!referencia) series.push([BR, `Brasil · ${seg.rotulo}`, COR_BRASIL]);
      const [ini, fim] = [seg.anos[0] as number, seg.anos.at(-1) as number];
      for (let a = ini; a <= fim; a++) {
        // Ano fora de `anos` vira null: o Plot quebra a linha ali (lacuna é lacuna).
        for (const [geo, serie, c] of series) {
          const p = seg.anos.includes(a) ? ponto(seg, geo, a) : undefined;
          // Num indicador todo estimado, "estimativa" vai no cabeçalho, não em cada ponto.
          const flags = (p?.flags ?? []).filter(
            (f) => !(ind.tipo_valor === 'estimativa' && f === 'estimativa'),
          );
          linhas.push({
            ano: a,
            v: p?.v ?? null,
            serie,
            rotulo: seg.rotulo,
            cor: c,
            marcado: flags.length > 0,
            detalhe: flags.map((f) => ROTULO_FLAG[f]).join('; '),
            referencia,
            bienal,
          });
        }
      }
    });

    this.#corpo.innerHTML = `
      <p class="painel-sub">${esc(nomeSub)} · ${esc(ind.unidade_detalhe)}${
        ind.tipo_valor === 'estimativa' ? ' · <strong>valores estimados, não medidos</strong>' : ''
      }</p>
      <dl class="painel-valores">
        <div><dt>${esc(uf.sigla)} em ${ano}</dt><dd>${esc(formatarValor(ind, pUf?.v))}</dd></div>
        <div><dt>Brasil em ${ano}</dt><dd>${esc(formatarValor(ind, pBr?.v))}</dd></div>
      </dl>
      <div class="grafico" role="img" aria-label="${esc(
        `Série de ${nomeSub} em ${uf.nome}, com o Brasil como referência`,
      )}"></div>
      <ul class="painel-legenda"></ul>
      <div class="painel-notas"></div>
      <p class="painel-sobre"><a href="indicador.html?i=${esc(ind.id)}">Sobre este indicador</a></p>`;

    const legenda = this.#corpo.querySelector('.painel-legenda') as HTMLElement;
    const series = [...new Map(linhas.map((l) => [l.serie, l])).entries()];
    legenda.innerHTML = series
      .map(
        ([s, l]) =>
          `<li><span class="traco${l.referencia || l.bienal ? ' tracejado' : ''}" style="--cor:${l.cor}"></span>${esc(s)}</li>`,
      )
      .join('');
    if (linhas.some((l) => l.bienal)) {
      legenda.innerHTML += `<li><span class="traco tracejado" style="--cor:#555"></span>dado a cada dois anos: o tracejado só liga os pontos, não há valor entre eles</li>`;
    }
    if (linhas.some((l) => l.marcado)) {
      legenda.innerHTML += `<li><span class="ponto-vazado"></span>ponto vazado = valor com ressalva (passe o mouse)</li>`;
    }

    const notas = this.#corpo.querySelector('.painel-notas') as HTMLElement;
    const quebras = (ind.quebras ?? []).map(
      (q) => `<li><strong>ⓘ ${q.ano}:</strong> ${esc(q.texto)}</li>`,
    );
    const notasSeg = segs
      .filter((s) => s.notas)
      .map((s) => `<li><strong>${esc(s.rotulo)}:</strong> ${esc(s.notas as string)}</li>`);
    notas.innerHTML =
      quebras.length || notasSeg.length ? `<ul>${[...quebras, ...notasSeg].join('')}</ul>` : '';

    const grafico = this.#corpo.querySelector('.grafico') as HTMLElement;
    const Plot = await import('@observablehq/plot');
    const fmt = (v: number) => formatarNumero(v, ind.casas_decimais);
    const comValor = linhas.filter((l) => l.v !== null);
    const largura = Math.max(280, grafico.clientWidth || 320);
    grafico.replaceChildren(
      Plot.plot({
        width: largura,
        height: 240,
        marginLeft: 56,
        style: { fontSize: '12px', background: 'transparent' },
        x: { label: null, tickFormat: (d: number) => String(d), ticks: 6 },
        y: { label: null, grid: true, tickFormat: fmt, zero: false },
        marks: [
          Plot.ruleX(ind.quebras ?? [], {
            x: (q: { ano: number }) => q.ano - 0.5,
            stroke: '#555',
            strokeDasharray: '4,3',
          }),
          Plot.text(ind.quebras ?? [], {
            x: (q: { ano: number }) => q.ano - 0.5,
            frameAnchor: 'top',
            text: () => 'ⓘ',
            title: (q: { texto: string }) => q.texto,
            fontSize: 14,
            dy: 2,
          }),
          Plot.lineY(
            linhas.filter((l) => !l.referencia),
            { x: 'ano', y: 'v', z: 'serie', stroke: 'cor', strokeWidth: 2 },
          ),
          Plot.lineY(
            linhas.filter((l) => l.referencia),
            {
              x: 'ano',
              y: 'v',
              z: 'serie',
              stroke: 'cor',
              strokeWidth: 1.5,
              strokeDasharray: '5,3',
            },
          ),
          Plot.lineY(
            comValor.filter((l) => l.bienal && !l.referencia),
            {
              x: 'ano',
              y: 'v',
              z: 'serie',
              stroke: 'cor',
              strokeWidth: 1.5,
              strokeDasharray: '3,3',
            },
          ),
          Plot.dot(comValor, {
            x: 'ano',
            y: 'v',
            stroke: 'cor',
            fill: (l: Linha) => (l.marcado ? '#ffffff' : l.cor),
            r: 3,
          }),
          Plot.tip(
            comValor,
            Plot.pointer({
              x: 'ano',
              y: 'v',
              title: (l: Linha) =>
                `${l.serie}\n${l.ano}: ${formatarValor(ind, l.v)}${l.detalhe ? `\n${l.detalhe}` : ''}${
                  l.bienal ? '\nDado bienal: não há valor nos anos vizinhos' : ''
                }`,
            }),
          ),
        ],
      }),
    );
    if (estavaFechado) this.#titulo.focus();
  }
}
