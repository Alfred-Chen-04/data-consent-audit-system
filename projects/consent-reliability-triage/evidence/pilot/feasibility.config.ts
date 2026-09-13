import { defineConfig, devices } from '@playwright/test';
export default defineConfig({
  testDir: './tests', testMatch: '_feasibility-pilot.spec.ts',
  workers: 1, retries: 0, timeout: 90000,
  outputDir: "/Users/alfred/Documents/ChatGPT/\u6570\u636e\u5408\u89c4/projects/consent-reliability-triage/evidence/pilot/test-results",
  reporter: [['list'], ['json', { outputFile: "/Users/alfred/Documents/ChatGPT/\u6570\u636e\u5408\u89c4/projects/consent-reliability-triage/evidence/pilot/playwright-report.json" }]],
  use: { ...devices['Desktop Chrome'], trace: 'off', screenshot: 'on', video: 'off' },
});
