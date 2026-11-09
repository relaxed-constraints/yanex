# Contributing

Clone the repository and install the locked development environment:

```bash
git clone https://github.com/relaxed-constraints/yanex.git
cd yanex
uv sync --all-extras --dev --group docs
```

Use a feature branch. Keep public API contracts in Google-style docstrings and
workflow explanations in the user guide. Include documentation changes with
user-facing behavior changes.

Before submitting:

```bash
uv run ruff check --fix
uv run ruff format
uv run ruff check
uv run pytest
uv run --group docs mkdocs build --strict
```

See [testing](testing.md), [architecture](architecture.md), and
[documentation maintenance](documentation.md).
