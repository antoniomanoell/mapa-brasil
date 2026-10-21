import { defineConfig } from 'vitest/config';

export default defineConfig({
  // Os JSON publicados pelo pipeline ficam em ../data/public e são servidos como estáticos.
  publicDir: '../data/public',
  // O MapLibre 6 carrega seu worker por URL relativa ao próprio módulo; a pré-otimização do
  // Vite (dev) move o arquivo e quebra esse caminho.
  optimizeDeps: { exclude: ['maplibre-gl'] },
  build: {
    // O MapLibre sozinho tem ~1 MB minificado (≈300 KB gzip); o orçamento real é o de 500 KB
    // comprimidos do carregamento inicial (PROJECT.md, 9.5).
    chunkSizeWarningLimit: 1200,
  },
  test: {
    include: ['tests/**/*.test.ts'],
  },
});
