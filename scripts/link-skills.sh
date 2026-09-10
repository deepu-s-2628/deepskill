#!/usr/bin/env bash
# Install itom-pm-skills into Claude Code by symlinking this repo's plugin
# directory into your local plugin cache. Re-run any time after a `git pull`
# to pick up new skills — existing symlinks are left alone.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_NAME="itom-pm-skills"
TARGET_DIR="${CLAUDE_PLUGINS_DIR:-$HOME/.claude/plugins/local}"

mkdir -p "$TARGET_DIR"
LINK_PATH="$TARGET_DIR/$PLUGIN_NAME"

if [ -e "$LINK_PATH" ]; then
  if [ -L "$LINK_PATH" ] && [ "$(readlink "$LINK_PATH")" = "$REPO_ROOT" ]; then
    echo "Already linked: $LINK_PATH -> $REPO_ROOT"
    exit 0
  fi
  echo "Refusing to overwrite existing path: $LINK_PATH" >&2
  echo "Remove it manually first if it's stale." >&2
  exit 1
fi

ln -s "$REPO_ROOT" "$LINK_PATH"
echo "Linked $LINK_PATH -> $REPO_ROOT"
echo "Restart Claude Code (or run /plugin reload if available) to pick it up."
