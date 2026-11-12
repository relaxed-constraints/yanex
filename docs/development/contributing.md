# Contributing

Clone the repository, then set up a development environment.

```bash
git clone https://github.com/relaxed-constraints/yanex.git
cd yanex
```

=== "uv"

    ```bash
    uv sync --locked --all-extras --dev --group docs
    ```

=== "pip"

    Activate a virtual environment as shown in [Installation](../getting-started/installation.md#install-yanex).

    ```bash
    python -m pip install --upgrade pip
    python -m pip install -e '.[dev,results]' --group dev --group docs
    ```

Use a feature branch. Keep public API contracts in Google-style docstrings and
workflow explanations in the user guide. Include documentation changes with
user-facing behavior changes.

Before submitting:

=== "uv"

    ```bash
    uv run ruff check --fix
    uv run ruff format
    uv run ruff check
    uv run pytest
    uv run --group docs zensical build --strict
    ```

=== "pip"

    ```bash
    ruff check --fix
    ruff format
    ruff check
    python -m pytest
    zensical build --strict
    ```

See [testing](testing.md), [architecture](architecture.md), and
[documentation maintenance](documentation.md). Maintainers should follow
[Building and releasing Yanex](releases.md) for distribution builds, PyPI setup,
release checks, and publication.
