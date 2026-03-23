#!/usr/bin/env bash
set -euo pipefail

REPO="gaspardip/skills"
CLAUDE_MD="$HOME/.claude/CLAUDE.md"
CLAUDE_DIR="$HOME/.claude"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "installing skills..."
npx skills add "$REPO@rubric" -g -y
npx skills add "$REPO@assess" -g -y
npx skills add "$REPO@deferred" -g -y

echo "installing commands..."
mkdir -p "$CLAUDE_DIR/commands"
for f in "$SCRIPT_DIR"/commands/*.md; do
  name=$(basename "$f")
  if [ -f "$CLAUDE_DIR/commands/$name" ]; then
    echo "  skip $name (already exists)"
  else
    cp "$f" "$CLAUDE_DIR/commands/$name"
    echo "  added $name"
  fi
done

echo "installing hookify rules..."
for f in "$SCRIPT_DIR"/hooks/*.local.md; do
  name=$(basename "$f")
  if [ -f "$CLAUDE_DIR/$name" ]; then
    echo "  skip $name (already exists)"
  else
    cp "$f" "$CLAUDE_DIR/$name"
    echo "  added $name"
  fi
done

echo "patching CLAUDE.md..."
for snippet in "$SCRIPT_DIR"/snippets/*.md; do
  # use first line as marker
  marker=$(head -1 "$snippet")
  if grep -qF "$marker" "$CLAUDE_MD" 2>/dev/null; then
    echo "  skip $(basename "$snippet") (already in CLAUDE.md)"
  else
    printf '\n' >> "$CLAUDE_MD"
    cat "$snippet" >> "$CLAUDE_MD"
    echo "  added $(basename "$snippet")"
  fi
done

echo "done."
