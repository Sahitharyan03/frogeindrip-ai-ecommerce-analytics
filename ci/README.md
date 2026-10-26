# Continuous Integration (GitHub Actions)

This folder contains the complete, production-ready GitHub Actions CI workflow for the Frogeindrip Analytics Platform:
- [`ci.yml`](file:///Users/sahit/Frogein%20drip/ci/ci.yml): Linting (Ruff), Unit Tests (Pytest), Deterministic DuckDB ETL Seeding, and dbt Integrity Tests (33 assertions).

---

## Activating the Workflow on GitHub Actions

If you want GitHub to automatically run this CI workflow on every push and pull request, GitHub requires your GitHub CLI token to have the `workflow` OAuth scope before pushing files directly inside `.github/workflows/`.

### Step 1: Add the `workflow` scope to GitHub CLI
Run this command in your terminal:
```bash
~/.local/bin/gh auth refresh -s workflow
```
Follow the one-time interactive browser prompt to authorize the workflow scope.

### Step 2: Move the workflow file and push
```bash
mkdir -p .github/workflows
git mv ci/ci.yml .github/workflows/ci.yml
git commit -m "ci: activate GitHub Actions workflow"
git push origin main
```

Your automated CI pipeline will immediately begin executing on GitHub Actions!
