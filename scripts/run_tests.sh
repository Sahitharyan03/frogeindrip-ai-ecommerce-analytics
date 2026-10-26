#!/usr/bin/env bash
set -e

echo "🔍 Running Ruff linter..."
.venv/bin/ruff check src/ app/ tests/

echo ""
echo "🧪 Running Pytest automated test suite..."
PYTHONPATH=src .venv/bin/pytest tests/ -v

echo ""
echo "📦 Running dbt data integrity tests..."
cd dbt && ../.venv/bin/dbt test --profiles-dir . && cd ..

echo ""
echo "✅ All tests passed successfully!"
