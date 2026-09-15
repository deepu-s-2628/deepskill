#!/usr/bin/env node
// npx skills add installs each skill as an independent, flattened package —
// it has no idea top-level context/ and scripts/ exist. skills/pm-shared/ is
// the sibling-installable mirror every other skill reads from after a flat
// install. This script is the one source of truth for keeping that mirror in
// sync with the canonical top-level context/ and scripts/ — run as part of
// `npm run version` (see package.json) alongside sync-plugin-version.mjs, so
// it can never drift the way marketplace.json's version once did.

import { readdirSync, readFileSync, writeFileSync, mkdirSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..');

const MIRRORS = [
  { source: 'context', dest: join('skills', 'pm-shared', 'context') },
  {
    source: 'scripts',
    dest: join('skills', 'pm-shared', 'scripts'),
    // .venv is a local dev artifact, never shipped. sync-plugin-version.mjs
    // and sync-pm-shared.mjs are dev-only tooling with no reason to exist
    // inside the installed mirror either.
    exclude: new Set(['.venv', 'sync-plugin-version.mjs', 'sync-pm-shared.mjs']),
  },
];

let changed = false;

for (const { source, dest, exclude } of MIRRORS) {
  const sourceDir = join(repoRoot, source);
  const destDir = join(repoRoot, dest);
  mkdirSync(destDir, { recursive: true });

  const files = readdirSync(sourceDir).filter((name) => {
    if (exclude?.has(name)) return false;
    return statSync(join(sourceDir, name)).isFile();
  });

  for (const name of files) {
    const sourcePath = join(sourceDir, name);
    const destPath = join(destDir, name);
    const content = readFileSync(sourcePath);
    let existing = null;
    try {
      existing = readFileSync(destPath);
    } catch {
      // dest doesn't exist yet — fine, we're about to write it.
    }
    if (existing && Buffer.compare(existing, content) === 0) {
      console.log(`${join(dest, name)} already in sync`);
      continue;
    }
    writeFileSync(destPath, content);
    changed = true;
    console.log(`synced ${join(source, name)} -> ${join(dest, name)}`);
  }
}

if (!changed) {
  console.log('skills/pm-shared/ already in sync with context/ and scripts/');
}
