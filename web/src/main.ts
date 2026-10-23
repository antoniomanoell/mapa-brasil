import './style.css';
import { criarControles } from './controls';
import { carregarCatalogo, carregarIndicador, carregarMalha } from './data';
import { formatarData } from './ficha';
import { esc } from './format';
import { renderLegenda } from './legend';
import { Mapa } from './map';
import { Painel } from './panel';
import { segmentoVigente } from './series';
import { Slider } from './slider';
import { SobreIndicador } from './sobre';
import { iniciarTema } from './tema';
import {
  type Estado,
  type EstadoBruto,
  Store,
  escreverUrl,
  indicadorPedido,
  lerUrl,
  normalizar,
} from './state';
import { renderResumo } from './resumo';
import { renderRanking } from './table';
import type { Catalogo, Indicador } from './types';
import { localPorSigla } from './ufs';

const $ = <T extends HTMLElement>(sel: string) => document.querySelector(sel) as T;

const paraBruto = (e: Estado): EstadoBruto => ({
  i: e.indicador,
  s: e.sub,
  a: String(e.ano),
  g: e.segmento,
  uf: e.uf,
  v: e.visao,
  sobre: e.sobre ? '1' : undefined,
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
  // A gaveta "Sobre" faz parte do estado (sobre=1 na URL): abre por link e fecha pelo ✕ ou Esc.
  const sobre = new SobreIndicador($('#sobre-indicador'), () => aplicar({ sobre: false }));
  let origemSobre: HTMLElement | null = null;
  // Links "Sobre este indicador" (barra, rodapé, painel) abrem a gaveta; sem JS, ou com Ctrl/
  // botão do meio, seguem para a página própria.
  document.addEventListener('click', (ev) => {
    const alvo = (ev.target as HTMLElement).closest<HTMLElement>('[data-abrir-sobre]');
    if (!alvo || ev.ctrlKey || ev.metaKey || ev.shiftKey || ev.button !== 0) return;
    ev.preventDefault();
    origemSobre = alvo;
    aplicar({ sobre: true });
  });
  // Computador: mapa e ranking lado a lado, sem a alternância Mapa/Ranking, e recortes em botões.
  const largo = matchMedia('(min-width: 960px)');
  const controles = criarControles(
    $('#controles'),
    largo,
    async (id) => {
      slider.parar();
      ind = await carregarIndicador(cat, id);
      // Mantém ano, UF e visão; subindicador e segmento voltam ao padrão do novo indicador.
      const e = store.estado;
      store.definir(
        normalizar(
          { i: id, a: String(e.ano), uf: e.uf, v: e.visao, sobre: e.sobre ? '1' : undefined },
          ind,
        ),
      );
    },
    (sub) => aplicar({ sub, segmento: undefined }),
    (uf) => aplicar({ uf }),
  );
  largo.addEventListener('change', () => {
    store.definir(store.estado);
    mapa.mapa.resize();
  });
  const alternarUf = (uf: string) => aplicar({ uf: store.estado.uf === uf ? undefined : uf });
  for (const b of document.querySelectorAll<HTMLButtonElement>('.visao button')) {
    b.addEventListener('click', () => aplicar({ visao: b.dataset['visao'] as Estado['visao'] }));
  }

  store.assinar((e, anterior) => renderizar(e, anterior, ind, cat));
  $('#atualizado').textContent = formatarData(cat.gerado_em);
  // Ao trocar o tema, o mapa e o gráfico do painel são redesenhados com as cores novas.
  iniciarTema(() => {
    void mapa.aplicarTema();
    store.definir(store.estado);
  });

  function renderizar(e: Estado, anterior: Estado | undefined, ind: Indicador, cat: Catalogo) {
    history.replaceState(null, '', escreverUrl(e, ind));
    atualizarMeta(e, ind);
    const seg = segmentoVigente(ind, e.sub, e.ano, e.segmento);

    controles.atualizar(cat, ind, e.sub, e.uf);
    renderResumo($('#resumo'), ind, seg, e.ano, e.uf, alternarUf);
    $('#abrir-sobre').setAttribute('href', `indicador.html?i=${encodeURIComponent(ind.id)}`);
    if (e.sobre && (!sobre.aberta || anterior?.indicador !== e.indicador)) {
      void sobre.abrir(ind, origemSobre);
      origemSobre = null;
    } else if (!e.sobre) {
      sobre.fechar();
    }
    slider.atualizar(ind, e.sub, e.ano, e.segmento);
    renderLegenda($('#legenda'), ind, e.sub);
    const nomeSub = ind.subindicadores.find((s) => s.id === e.sub)?.nome ?? ind.nome;
    $('#titulo-mapa').textContent = `${nomeSub} em ${e.ano}`;
    void mapa.atualizar({ ind, sub: e.sub, ano: e.ano, seg, uf: e.uf });

    for (const b of document.querySelectorAll<HTMLButtonElement>('.visao button')) {
      b.setAttribute('aria-pressed', String(b.dataset['visao'] === e.visao));
    }
    const lado = largo.matches;
    $('#mapa-area').hidden = !lado && e.visao !== 'mapa';
    $('#ranking').hidden = !lado && e.visao !== 'ranking';
    if (lado || e.visao === 'ranking') {
      renderRanking($('#ranking'), ind, seg, e.ano, e.uf, (uf) => aplicar({ uf }));
    }
    if (!lado && e.visao === 'mapa' && anterior?.visao === 'ranking') mapa.mapa.resize();

    if (e.uf) void painel.abrir(ind, e.sub, e.ano, e.segmento, e.uf);
    else painel.fechar();

    const rodape = $('#rodape-viz');
    rodape.innerHTML = seg
      ? `<p><strong>Fonte:</strong> <a href="${esc(seg.fonte_url)}" rel="noopener">${esc(seg.fonte)}</a>
          · ${esc(seg.tabela)} · extraído em ${esc(formatarData(seg.extraido_em))}</p>
         <p>${esc(ind.unidade_detalhe)}.${seg.notas ? ` ${esc(seg.notas)}` : ''}</p>`
      : `<p>Não há dado deste indicador em ${e.ano}.</p>`;
    rodape.innerHTML += `<p><a href="indicador.html?i=${esc(ind.id)}" data-abrir-sobre>Sobre este indicador: o que mede, como ler e limitações</a></p>`;
  }

  store.definir(normalizar(bruto, ind));
  await mapa.pronto;
  // Gancho para os testes de fumaça (Playwright): centro de uma UF em pixels do mapa.
  (window as unknown as Record<string, unknown>)['__centroUF'] = (sigla: string) =>
    mapa.centroEmPixels(sigla);
  document.body.dataset['pronto'] = 'true';
}

function atualizarMeta(e: Estado, ind: Indicador): void {
  const nomeSub = ind.subindicadores.find((s) => s.id === e.sub)?.nome ?? ind.nome;
  const uf = e.uf ? localPorSigla(e.uf)?.nome : undefined;
  document.title = `${nomeSub} · ${e.ano}${uf ? ` · ${uf}` : ''} — Indicadores BR`;
  const desc = `${nomeSub} ${uf ? `em ${uf}` : 'por estado'} em ${e.ano}, com dados oficiais. ${ind.unidade_detalhe}.`;
  document.querySelector('meta[name="description"]')?.setAttribute('content', desc);
}

iniciar().catch((erro: unknown) => {
  console.error(erro);
  $('#erro').hidden = false;
});
