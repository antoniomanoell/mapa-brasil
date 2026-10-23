// Mapa coroplético das UFs: MapLibre sem mapa-base, só os polígonos (PROJECT.md, 5.1).

import {
  LngLatBounds,
  Map as MapaGL,
  type MapLayerMouseEvent,
  Marker,
  NavigationControl,
  setWorkerUrl,
} from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
// O MapLibre procura o worker como arquivo vizinho do próprio módulo, o que o bundler não vê.
// Importá-lo como worker faz o Vite empacotá-lo (com as dependências) e dá a URL final.
import urlWorker from 'maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url';
import { feature } from 'topojson-client';
import type { Topology } from 'topojson-specification';
import { CORES, hachura } from './cores';
import { cor } from './tema';
import { ROTULO_FLAG, esc, formatarValor } from './format';
import { classe, ponto } from './series';
import type { Indicador, Segmento } from './types';
import { UFS, ufPorCodigo, ufPorSigla } from './ufs';

setWorkerUrl(urlWorker);

const LIMITES_BR: [[number, number], [number, number]] = [
  [-74.2, -33.9],
  [-28.6, 5.4],
];

// Onde escrever a sigla de cada UF (lng, lat): o centro visual, não o da caixa, que cai fora de
// estados recortados. GO sai um pouco do centro para não encostar no DF; os estados pequenos da
// costa (FORA) têm a sigla no mar, ao lado, onde não se sobrepõem.
const ROTULOS: Record<string, [number, number]> = {
  RO: [-62.8, -10.9],
  AC: [-70.5, -9.1],
  AM: [-64.6, -4.2],
  RR: [-61.3, 2.0],
  PA: [-52.5, -4.0],
  AP: [-51.9, 1.4],
  TO: [-48.3, -10.2],
  MA: [-45.3, -5.0],
  PI: [-42.9, -7.4],
  CE: [-39.5, -5.2],
  RN: [-34.6, -5.2],
  PB: [-34.0, -7.1],
  PE: [-34.0, -8.4],
  AL: [-34.6, -9.8],
  SE: [-35.8, -11.3],
  BA: [-41.7, -12.5],
  MG: [-44.6, -18.5],
  ES: [-38.9, -20.0],
  RJ: [-41.9, -23.6],
  SP: [-48.7, -22.2],
  PR: [-51.6, -24.6],
  SC: [-50.4, -27.2],
  RS: [-53.3, -29.7],
  MS: [-54.8, -20.5],
  MT: [-55.9, -12.9],
  GO: [-50.8, -16.6],
  // DF é pequeno demais para a sigla caber dentro: ela fica logo ao lado, à direita.
  DF: [-46.75, -15.75],
};
const FORA = new Set(['RN', 'PB', 'PE', 'AL', 'SE', 'ES', 'RJ', 'DF']);
// Classes a partir desta (as duas mais escuras) levam a sigla em branco.
const CLASSE_ESCURA = 3;

export interface Vista {
  ind: Indicador;
  sub: string;
  ano: number;
  seg: Segmento | undefined;
  uf: string | undefined;
}

export class Mapa {
  readonly mapa: MapaGL;
  readonly pronto: Promise<void>;
  #dica: HTMLDivElement;
  #vista: Vista | undefined;
  #geo: GeoJSON.FeatureCollection;
  #rotulos = new Map<string, HTMLSpanElement>();

  constructor(container: HTMLElement, topo: unknown, aoSelecionar: (sigla: string) => void) {
    const t = topo as Topology;
    const geo = feature(t, t.objects['BRUF'] as never) as unknown as GeoJSON.FeatureCollection;
    this.#geo = geo;
    this.mapa = new MapaGL({
      container,
      style: {
        version: 8,
        sources: {},
        layers: [
          { id: 'fundo', type: 'background', paint: { 'background-color': cor('--fundo') } },
        ],
      },
      bounds: LIMITES_BR,
      fitBoundsOptions: { padding: 8 },
      attributionControl: false,
      dragRotate: false,
      pitchWithRotate: false,
      touchPitch: false,
      renderWorldCopies: false,
      maxZoom: 7,
      minZoom: 2,
      // A roda do mouse e o arrasto com um dedo rolam a página; o zoom pede Ctrl/⌘ + roda, dois
      // dedos ou os botões + e −.
      cooperativeGestures: true,
      locale: {
        'CooperativeGesturesHandler.WindowsHelpText': 'Use Ctrl + roda do mouse para dar zoom',
        'CooperativeGesturesHandler.MacHelpText': 'Use ⌘ + roda do mouse para dar zoom',
        'CooperativeGesturesHandler.MobileHelpText': 'Use dois dedos para mover o mapa',
        'NavigationControl.ZoomIn': 'Aproximar',
        'NavigationControl.ZoomOut': 'Afastar',
      },
    });
    this.mapa.addControl(new NavigationControl({ showCompass: false }), 'top-right');
    this.mapa.touchZoomRotate.disableRotation();
    this.mapa.keyboard.disableRotation();

    this.#dica = document.createElement('div');
    this.#dica.className = 'dica';
    this.#dica.hidden = true;
    container.append(this.#dica);

    this.pronto = new Promise((resolve) => {
      this.mapa.on('load', () => {
        this.mapa.addImage('hachura', hachura(cor('--hachura-fundo'), cor('--hachura-linha')), {
          pixelRatio: 2,
        });
        this.mapa.addSource('ufs', { type: 'geojson', data: geo, promoteId: 'codarea' });
        const corClasse = [
          'match',
          ['feature-state', 'classe'],
          ...CORES.flatMap((c, i) => [i, c]),
          '#000',
        ];
        this.mapa.addLayer({
          id: 'ufs-hachura',
          type: 'fill',
          source: 'ufs',
          paint: { 'fill-pattern': 'hachura' },
        });
        this.mapa.addLayer({
          id: 'ufs-cor',
          type: 'fill',
          source: 'ufs',
          paint: {
            'fill-color': corClasse as never,
            'fill-opacity': [
              'case',
              ['>=', ['coalesce', ['feature-state', 'classe'], -1], 0],
              1,
              0,
            ],
          },
        });
        this.mapa.addLayer({
          id: 'ufs-borda',
          type: 'line',
          source: 'ufs',
          paint: { 'line-color': cor('--fundo'), 'line-width': 0.8 },
        });
        this.mapa.addLayer({
          id: 'ufs-selecao',
          type: 'line',
          source: 'ufs',
          paint: {
            'line-color': cor('--mapa-contorno-sel'),
            'line-width': ['case', ['boolean', ['feature-state', 'sel'], false], 2.5, 0],
          },
        });
        // Pronto só depois que o worker processou os polígonos e o primeiro quadro foi desenhado.
        // As siglas entram junto, para não aparecerem soltas sobre o mapa ainda vazio.
        this.mapa.once('idle', () => {
          this.#criarRotulos();
          resolve();
        });
      });
    });

    this.mapa.on('mousemove', 'ufs-hachura', (e) => this.#mostrarDica(e));
    this.mapa.on('mouseleave', 'ufs-hachura', () => {
      this.#dica.hidden = true;
      this.mapa.getCanvas().style.cursor = '';
    });
    this.mapa.on('click', 'ufs-hachura', (e) => {
      const uf = ufPorCodigo(String(e.features?.[0]?.properties?.['codarea']));
      if (uf) aoSelecionar(uf.sigla);
    });
  }

  /** Redesenha fundo, divisas, seleção e hachura com as cores do tema atual. */
  async aplicarTema(): Promise<void> {
    await this.pronto;
    this.mapa.setPaintProperty('fundo', 'background-color', cor('--fundo'));
    this.mapa.setPaintProperty('ufs-borda', 'line-color', cor('--fundo'));
    this.mapa.setPaintProperty('ufs-selecao', 'line-color', cor('--mapa-contorno-sel'));
    this.mapa.updateImage('hachura', hachura(cor('--hachura-fundo'), cor('--hachura-linha')));
  }

  async atualizar(vista: Vista): Promise<void> {
    await this.pronto;
    this.#vista = vista;
    const limites = vista.ind.escalas[vista.sub]?.limites ?? [];
    const sel = vista.uf ? ufPorSigla(vista.uf)?.codigo : undefined;
    for (const uf of UFS) {
      const v = ponto(vista.seg, uf.codigo, vista.ano)?.v;
      const c = v === null || v === undefined ? -1 : classe(v, limites);
      this.mapa.setFeatureState(
        { source: 'ufs', id: uf.codigo },
        { classe: c, sel: uf.codigo === sel },
      );
      this.#rotulos
        .get(uf.sigla)
        ?.classList.toggle('escuro', c >= CLASSE_ESCURA && !FORA.has(uf.sigla));
    }
  }

  /** Siglas das UFs. São marcadores HTML (a fonte da página), não uma camada de texto do MapLibre,
   *  que exigiria baixar fontes de um servidor externo. Não recebem o mouse: o clique vai à UF. */
  #criarRotulos(): void {
    for (const uf of UFS) {
      const pos = ROTULOS[uf.sigla];
      if (!pos) continue;
      const el = document.createElement('span');
      el.className = 'rotulo-uf';
      el.textContent = uf.sigla;
      el.setAttribute('aria-hidden', 'true');
      new Marker({ element: el }).setLngLat(pos).addTo(this.mapa);
      this.#rotulos.set(uf.sigla, el);
    }
  }

  /** Centro de uma UF em pixels da tela (usado nos testes de fumaça). */
  centroEmPixels(sigla: string): { x: number; y: number } | undefined {
    const codigo = ufPorSigla(sigla)?.codigo;
    const f = this.#geo.features.find((x) => x.properties?.['codarea'] === codigo);
    if (!f) return undefined;
    const b = new LngLatBounds();
    const g = f.geometry as GeoJSON.Polygon | GeoJSON.MultiPolygon;
    const aneis = g.type === 'Polygon' ? [g.coordinates[0]] : g.coordinates.map((p) => p[0]);
    for (const anel of aneis) for (const c of anel ?? []) b.extend(c as [number, number]);
    const p = this.mapa.project(b.getCenter());
    return { x: p.x, y: p.y };
  }

  #mostrarDica(e: MapLayerMouseEvent): void {
    const v = this.#vista;
    const codigo = String(e.features?.[0]?.properties?.['codarea']);
    const uf = ufPorCodigo(codigo);
    if (!v || !uf) return;
    this.mapa.getCanvas().style.cursor = 'pointer';
    const p = ponto(v.seg, codigo, v.ano);
    const flags = (p?.flags ?? []).map((f) => `<li>${ROTULO_FLAG[f]}</li>`).join('');
    this.#dica.innerHTML =
      `<strong>${esc(uf.nome)}</strong>` +
      `<span class="dica-valor">${esc(formatarValor(v.ind, p?.v))}</span>` +
      `<span class="dica-meta">${v.ano}${v.seg ? ` · ${esc(v.seg.rotulo)}` : ''}</span>` +
      (p?.lacuna ? `<span class="dica-meta">${esc(p.lacuna)}</span>` : '') +
      (flags ? `<ul class="dica-flags">${flags}</ul>` : '');
    const { x, y } = e.point;
    const largura = this.mapa.getContainer().clientWidth;
    this.#dica.style.left = `${Math.min(x + 12, largura - 220)}px`;
    this.#dica.style.top = `${y + 12}px`;
    this.#dica.hidden = false;
  }
}
