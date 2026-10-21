import { defineConfig, devices } from '@playwright/test';

const PORTA = 4173;

export default defineConfig({
  testDir: 'e2e',
  // WebGL por software (SwiftShader) é lento no CI, sobretudo no perfil de celular (DPR alto).
  timeout: process.env['CI'] ? 90_000 : 30_000,
  retries: process.env['CI'] ? 1 : 0,
  reporter: process.env['CI'] ? [['github'], ['html', { open: 'never' }]] : 'list',
  use: {
    trace: 'retain-on-failure',
    baseURL: `http://localhost:${PORTA}`,
    // WebGL no headless sem GPU.
    launchOptions: { args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] },
  },
  projects: [
    {
      name: 'desktop',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 800 } },
    },
    { name: 'celular', use: { ...devices['Pixel 7'] } },
  ],
  webServer: {
    command: `npm run build && npx vite preview --port ${PORTA} --strictPort`,
    port: PORTA,
    reuseExistingServer: !process.env['CI'],
    timeout: 120_000,
  },
});
