#!/usr/bin/env node
// Changesets bumps package.json's version but has no idea .claude-plugin/plugin.json
// exists — that's the manifest npx skills add reads to discover what's installable.
// Run as part of `npm run version` (see package.json) so the two never drift again.

import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const pkg = JSON.parse(readFileSync(join(repoRoot, 'package.json'), 'utf8'));

function syncVersion(relativePath) {
  const filePath = join(repoRoot, relativePath);
  const text = readFileSync(filePath, 'utf8');
  const updated = text.replace(
    /"version":\s*"[^"]*"/,
    `"version": "${pkg.version}"`
  );
  if (updated === text) {
    console.log(`${relativePath} already at ${pkg.version}`);
  } else {
    writeFileSync(filePath, updated);
    console.log(`synced ${relativePath} version -> ${pkg.version}`);
  }
}

syncVersion(join('.claude-plugin', 'plugin.json'));
