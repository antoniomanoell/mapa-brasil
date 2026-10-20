import { defineConfig } from 'vitest/config';

export default defineConfig({
  // Os JSON publicados pelo pipeline ficam em ../data/public e são servidos como estáticos.
  publicDir: '../data/public',
  test: {
    include: ['tests/**/*.test.ts'],
  },
});
