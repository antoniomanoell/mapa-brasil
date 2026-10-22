// Mapa coroplético das UFs: MapLibre sem mapa-base, só os polígonos (PROJECT.md, 5.1).

import {
  LngLatBounds,
  Map as MapaGL,
  type MapLayerMouseEvent,
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
import { ROTULO_FLAG, esc, formatarValor } from './format';
import { classe, ponto } from './series';
import type { Indicador, Segmento } from './types';
import { UFS, ufPorCodigo, ufPorSigla } from './ufs';

setWorkerUrl(urlWorker);

const LIMITES_BR: [[number, number], [number, number]] = [
  [-74.2, -33.9],
  [-28.6, 5.4],
];

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

  constructor(container: HTMLElement, topo: unknown, aoSelecionar: (sigla: string) => void) {
    const t = topo as Topology;
    const geo = feature(t, t.objects['BRUF'] as never) as unknown as GeoJSON.FeatureCollection;
    this.#geo = geo;
    this.mapa = new MapaGL({
      container,
      style: {
        version: 8,
        sources: {},
        layers: [{ id: 'fundo', type: 'background', paint: { 'background-color': '#ffffff' } }],
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
        this.mapa.addImage('hachura', hachura(), { pixelRatio: 2 });
        this.mapa.addSource('ufs', { type: 'geojson', data: geo, promoteId: 'codarea' });
        const cor = [
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
            'fill-color': cor as never,
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
          paint: { 'line-color': '#ffffff', 'line-width': 0.8 },
        });
        this.mapa.addLayer({
          id: 'ufs-selecao',
          type: 'line',
          source: 'ufs',
          paint: {
            'line-color': '#111111',
            'line-width': ['case', ['boolean', ['feature-state', 'sel'], false], 2.5, 0],
          },
        });
        // Pronto só depois que o worker processou os polígonos e o primeiro quadro foi desenhado.
        this.mapa.once('idle', () => resolve());
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

  async atualizar(vista: Vista): Promise<void> {
    await this.pronto;
    this.#vista = vista;
    const limites = vista.ind.escalas[vista.sub]?.limites ?? [];
    const sel = vista.uf ? ufPorSigla(vista.uf)?.codigo : undefined;
    for (const uf of UFS) {
      const v = ponto(vista.seg, uf.codigo, vista.ano)?.v;
      this.mapa.setFeatureState(
        { source: 'ufs', id: uf.codigo },
        { classe: v === null || v === undefined ? -1 : classe(v, limites), sel: uf.codigo === sel },
      );
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
