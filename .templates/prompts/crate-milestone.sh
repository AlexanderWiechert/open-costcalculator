#!/bin/bash

# GitHub-Repo
REPO="AlexanderWiechert/open-costcalculator"
MILESTONE="MVP: Analyzer & Config Support (Q3 2025)"

# Liste der relevanten Spez-Dateien (anpassen falls nötig)
FILES=(
  "spec/iusse-created/spec-core-refactor-logging.md"
  "spec/iusse-created/modularize-main.md"
  "spec/iusse-created/use-logging.md"
  "spec/iusse-created/centralize-region-config.md"
  "spec/iusse-created/spec-config-support.md"
  "spec/iusse-created/spec-aws-s3-analyzer.md"
  "spec/iusse-created/spec-aws-ecs-analyzer.md"
  "spec/iusse-created/spec-aws-lb-analyzer.md"
  "spec/iusse-created/refactor-report-output.md"
)

# Durchlaufe jede Datei
for FILE in "${FILES[@]}"; do
  TITLE=$(grep '^# ' "$FILE" | head -n 1 | sed 's/^# //')
  ISSUE=$(gh issue list --repo "$REPO" --state open --search "$TITLE" --json number --jq '.[0].number')
  if [ -n "$ISSUE" ]; then
    echo "✅ Zuweisung: #$ISSUE → $MILESTONE"
    gh issue edit "$ISSUE" --repo "$REPO" --milestone "$MILESTONE"
  else
    echo "⚠️  Kein Issue gefunden für: $TITLE"
  fi
done
