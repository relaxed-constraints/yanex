# Testing

```bash
uv run pytest
uv run pytest tests/core/ -n 0
```

Tests run in parallel by default. Use `-n 0` for sequential debugging. The suite
records coverage and uses temporary experiment stores and Git repositories.

Release CI tests Python 3.11 and 3.12 sequentially and temporarily requires at
least **80%** Python coverage:

```bash
uv run pytest --cov=yanex --cov-report=term-missing --cov-fail-under=80 -n 0
```

Use the missing-line report to select meaningful untested behaviours, particularly
failure handling and user-facing contracts. Keep the threshold in sync with
`.github/workflows/release-checks.yml`. See [the release guide](releases.md) for
frontend checks and installed-package verification.

For CLI integration tests, use `per_test_experiments_dir` to isolate storage and
reset the Results API's cached manager. `clean_api_state` isolates Run API state.
Avoid pointing tests at a real research store.

A strict MkDocs build checks documentation links and API-object resolution. It does
not execute ordinary fenced examples. Check changed examples separately in an
isolated store, then remove probe data.
