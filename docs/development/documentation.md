# Building and publishing documentation

There is one documentation source tree: `docs/`, organised like the site navigation
in `mkdocs.yml`. Python API contracts live in source docstrings and are rendered by
mkdocstrings. Do not copy generated signatures and parameter lists into guides.
Examples stay beside their runnable scripts and are linked from the site.

## Preview and validate

```bash
uv sync --locked --group docs
uv run --group docs mkdocs serve
uv run --group docs mkdocs build --strict
```

The preview is served at `http://127.0.0.1:8000/yanex/`. The build writes to the
ignored `site/` directory. Source changes also trigger preview rebuilds.

Material uses the same settings as BONDI: system fonts, navigation tabs, a back-to-top
button, syntax highlighting, and code-copy buttons.

## Markdown lists

Leave a blank line between introductory text and a bulleted or numbered list.
This also applies to Markdown inside Python docstrings, including parameter
descriptions. Without that separator, MkDocs can render list markers as ordinary
paragraph text even when GitHub displays them as a list.

## API reference

Add or improve Google-style `Args`, `Returns`, `Raises`, and `Examples` sections
beside the implementation. Reference pages explicitly select public objects:

```text
::: yanex.log_metrics
```

Keep examples executable in the documented context. A strict build validates
rendering and links, but does not execute code blocks or prove behavioral claims.

## GitHub Pages

The documentation check runs on pushes and pull requests. Publishing is separate:
`.github/workflows/pages.yml` deploys on a published release or manual dispatch,
matching BONDI's policy. It does not deploy on every merge to `main`.

Configure the repository's **Settings → Pages → Source** as **GitHub Actions**.
The workflow builds the checked-out release tag (or manually selected ref), uploads
`site/`, and deploys with the `github-pages` environment. Ensure that environment's
branch/tag rules allow the release tags and the intended manual-dispatch branch.

The site URL is `https://relaxed-constraints.github.io/yanex/`. A single published site tracks
the last deployed release/ref; historical version sites are not generated.
