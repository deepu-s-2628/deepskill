#!/usr/bin/env node
// Changesets bumps package.json's version but has no idea .claude-plugin/plugin.json
// exists — that's the manifest that actually matters for the installed plugin.
// Run as part of `npm run version` (see package.json) so the two never drift again.

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const pkg = JSON.parse(readFileSync(join(repoRoot, 'package.json'), 'utf8'));
const pluginPath = join(repoRoot, '.claude-plugin', 'plugin.json');
const pluginText = readFileSync(pluginPath, 'utf8');

const updated = pluginText.replace(
  /"version":\s*"[^"]*"/,
  `"version": "${pkg.version}"`
);

if (updated === pluginText) {
  console.log(`plugin.json already at ${pkg.version}`);
} else {
  writeFileSync(pluginPath, updated);
  console.log(`synced plugin.json version -> ${pkg.version}`);
}
