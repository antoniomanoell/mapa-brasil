import { cpSync, existsSync, readFileSync, statSync } from 'node:fs';
import { extname, join, resolve } from 'node:path';
import { type Plugin, loadEnv } from 'vite';
import { defineConfig } from 'vitest/config';

// Saída do pipeline (catálogo, indicadores, malha). Fica fora de web/public: é dado, não asset.
const DADOS = resolve(import.meta.dirname, '../data/public');
const TIPOS: Record<string, string> = {
  '.json': 'application/json',
  '.topojson': 'application/json',
};

/** Serve data/public no dev/preview e o copia para dist/ no build, nos mesmos caminhos. */
function dadosPublicados(): Plugin {
  const servir = (
    req: { url?: string },
    res: { setHeader(k: string, v: string): void; end(b: Buffer): void },
    next: () => void,
  ) => {
    const caminho = join(DADOS, decodeURIComponent((req.url ?? '').split('?')[0] ?? ''));
    if (!caminho.startsWith(DADOS) || !existsSync(caminho) || !statSync(caminho).isFile()) {
      return next();
    }
    res.setHeader('Content-Type', TIPOS[extname(caminho)] ?? 'application/octet-stream');
    res.end(readFileSync(caminho));
  };
  let saida = 'dist';
  return {
    name: 'dados-publicados',
    configResolved(c) {
      saida = resolve(c.root, c.build.outDir);
    },
    configureServer(server) {
      server.middlewares.use(servir);
    },
    closeBundle() {
      cpSync(DADOS, saida, { recursive: true });
    },
  };
}

/** Cloudflare Web Analytics (sem cookies), só se houver token em VITE_CF_BEACON_TOKEN. */
function analytics(token: string): Plugin {
  return {
    name: 'analytics',
    transformIndexHtml() {
      if (!token) return [];
      return [
        {
          tag: 'script',
          attrs: {
            defer: true,
            src: 'https://static.cloudflareinsights.com/beacon.min.js',
            'data-cf-beacon': JSON.stringify({ token }),
          },
          injectTo: 'body',
        },
      ];
    },
  };
}

export default defineConfig(({ mode }) => ({
  plugins: [
    dadosPublicados(),
    analytics(loadEnv(mode, import.meta.dirname, 'VITE_')['VITE_CF_BEACON_TOKEN'] ?? ''),
  ],
  // O MapLibre 6 carrega seu worker por URL relativa ao próprio módulo; a pré-otimização do
  // Vite (dev) move o arquivo e quebra esse caminho.
  optimizeDeps: { exclude: ['maplibre-gl'] },
  // O worker do MapLibre é um módulo ES.
  worker: { format: 'es' },
  build: {
    // O MapLibre sozinho tem ~1 MB minificado (≈300 KB gzip); o orçamento real é o de 500 KB
    // comprimidos do carregamento inicial (PROJECT.md, 9.5).
    chunkSizeWarningLimit: 1200,
    rollupOptions: {
      input: {
        index: resolve(import.meta.dirname, 'index.html'),
        indicador: resolve(import.meta.dirname, 'indicador.html'),
        metodologia: resolve(import.meta.dirname, 'metodologia.html'),
        sobre: resolve(import.meta.dirname, 'sobre.html'),
      },
    },
  },
  test: {
    include: ['tests/**/*.test.ts'],
  },
}));
