import './style.css';
import { criarControles } from './controls';
import { carregarCatalogo, carregarIndicador, carregarMalha } from './data';
import { esc } from './format';
import { renderLegenda } from './legend';
import { Mapa } from './map';
import { Painel } from './panel';
import { segmentoVigente } from './series';
import { Slider } from './slider';
import {
  type Estado,
  type EstadoBruto,
  Store,
  escreverUrl,
  indicadorPedido,
  lerUrl,
  normalizar,
} from './state';
import { renderRanking } from './table';
import type { Catalogo, Indicador } from './types';
import { ufPorSigla } from './ufs';

const $ = <T extends HTMLElement>(sel: string) => document.querySelector(sel) as T;

const paraBruto = (e: Estado): EstadoBruto => ({
  i: e.indicador,
  s: e.sub,
  a: String(e.ano),
  g: e.segmento,
  uf: e.uf,
  v: e.visao,
});

async function iniciar(): Promise<void> {
  const [cat, topo] = await Promise.all([carregarCatalogo(), carregarMalha()]);
  const bruto = lerUrl(location.search);
  let ind = await carregarIndicador(cat, indicadorPedido(bruto, cat));
  const store = new Store();

  // Toda mudança passa por normalizar(): segmento que não vale no ano novo, por exemplo, cai.
  const aplicar = (parcial: Partial<Estado>) =>
    store.definir(normalizar(paraBruto({ ...store.estado, ...parcial }), ind));

  const mapa = new Mapa($('#mapa'), topo, (uf) => aplicar({ uf }));
  const slider = new Slider(
    $('#slider'),
    (ano) => aplicar({ ano }),
    (segmento) => aplicar({ segmento }),
  );
  const painel = new Painel($('#painel'), () => aplicar({ uf: undefined }));
  const controles = criarControles(
    $('#controles'),
    async (id) => {
      slider.parar();
      ind = await carregarIndicador(cat, id);
      // Mantém ano, UF e visão; subindicador e segmento voltam ao padrão do novo indicador.
      const e = store.estado;
      store.definir(normalizar({ i: id, a: String(e.ano), uf: e.uf, v: e.visao }, ind));
    },
    (sub) => aplicar({ sub, segmento: undefined }),
    (uf) => aplicar({ uf }),
  );
  for (const b of document.querySelectorAll<HTMLButtonElement>('.visao button')) {
    b.addEventListener('click', () => aplicar({ visao: b.dataset['visao'] as Estado['visao'] }));
  }

  store.assinar((e, anterior) => renderizar(e, anterior, ind, cat));

  function renderizar(e: Estado, anterior: Estado | undefined, ind: Indicador, cat: Catalogo) {
    history.replaceState(null, '', escreverUrl(e, ind));
    atualizarMeta(e, ind);
    const seg = segmentoVigente(ind, e.sub, e.ano, e.segmento);

    controles.atualizar(cat, ind, e.sub, e.uf);
    slider.atualizar(ind, e.sub, e.ano, e.segmento);
    renderLegenda($('#legenda'), ind, e.sub);
    void mapa.atualizar({ ind, sub: e.sub, ano: e.ano, seg, uf: e.uf });

    for (const b of document.querySelectorAll<HTMLButtonElement>('.visao button')) {
      b.setAttribute('aria-pressed', String(b.dataset['visao'] === e.visao));
    }
    $('#mapa-area').hidden = e.visao !== 'mapa';
    $('#ranking').hidden = e.visao !== 'ranking';
    if (e.visao === 'ranking') {
      renderRanking($('#ranking'), ind, seg, e.ano, e.uf, (uf) => aplicar({ uf }));
    } else if (anterior?.visao === 'ranking') {
      mapa.mapa.resize();
    }

    if (e.uf) void painel.abrir(ind, e.sub, e.ano, e.segmento, e.uf);
    else painel.fechar();

    const rodape = $('#rodape-viz');
    rodape.innerHTML = seg
      ? `<p><strong>Fonte:</strong> <a href="${esc(seg.fonte_url)}" rel="noopener">${esc(seg.fonte)}</a>
          · ${esc(seg.tabela)} · extraído em ${esc(formatarData(seg.extraido_em))}</p>
         <p>${esc(ind.unidade_detalhe)}.${seg.notas ? ` ${esc(seg.notas)}` : ''}</p>`
      : `<p>Não há dado deste indicador em ${e.ano}.</p>`;
    rodape.innerHTML += `<p><a href="indicador.html?i=${esc(ind.id)}">Sobre este indicador: o que mede, como ler e limitações</a></p>`;
  }

  store.definir(normalizar(bruto, ind));
  await mapa.pronto;
  // Gancho para os testes de fumaça (Playwright): centro de uma UF em pixels do mapa.
  (window as unknown as Record<string, unknown>)['__centroUF'] = (sigla: string) =>
    mapa.centroEmPixels(sigla);
  document.body.dataset['pronto'] = 'true';
}

function formatarData(iso: string): string {
  const [a, m, d] = iso.split('-');
  return `${d}/${m}/${a}`;
}

function atualizarMeta(e: Estado, ind: Indicador): void {
  const nomeSub = ind.subindicadores.find((s) => s.id === e.sub)?.nome ?? ind.nome;
  const uf = e.uf ? ufPorSigla(e.uf)?.nome : undefined;
  document.title = `${nomeSub} · ${e.ano}${uf ? ` · ${uf}` : ''} — Indicadores BR`;
  const desc = `${nomeSub} ${uf ? `em ${uf}` : 'por estado'} em ${e.ano}, com dados oficiais. ${ind.unidade_detalhe}.`;
  document.querySelector('meta[name="description"]')?.setAttribute('content', desc);
}

iniciar().catch((erro: unknown) => {
  console.error(erro);
  $('#erro').hidden = false;
});
