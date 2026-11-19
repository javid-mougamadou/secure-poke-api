#!/bin/bash

set -e

# Usage : ./scripts/lint.sh [dossier]
#   ./scripts/lint.sh       -> cible tout le projet
#   ./scripts/lint.sh config -> cible un module spécifique
TARGET="${1:-.}"

echo "Running isort..."
uv run isort "$TARGET"

echo "Running black..."
uv run black "$TARGET"

echo "Running ruff format..."
uv run ruff format "$TARGET"

echo "Running ruff check..."
uv run ruff check "$TARGET"

echo "All checks passed!"
