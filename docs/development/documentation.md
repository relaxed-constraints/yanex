# Building and publishing documentation

There is one documentation source tree: `docs/`, organised like the site navigation
in `mkdocs.yml`. Python API contracts live in source docstrings and are rendered by
mkdocstrings. Do not copy generated signatures and parameter lists into guides.
Examples stay beside their runnable scripts and are linked from the site.

## Preview and validate

=== "uv"

    ```bash
    uv sync --locked --group docs
    uv run --group docs zensical serve
    uv run --group docs zensical build --strict
    ```

=== "pip"

    In an activated virtual environment, upgrade pip to enable dependency groups.

    ```bash
    python -m pip install --upgrade pip
    python -m pip install --group docs
    zensical serve
    zensical build --strict
    ```

Open the preview URL printed in the terminal. Run the strict build in a
separate terminal or after stopping the server. The output goes to `site/`.

Zensical uses the modern theme with system fonts, a light and dark mode toggle,
linked uv and pip tabs, search highlighting, and code-copy buttons. Mermaid
diagrams use Zensical’s built-in integration.

## Markdown lists

Leave a blank line between introductory text and a bulleted or numbered list.
This also applies to Markdown inside Python docstrings, including parameter
descriptions. Without that separator, Zensical can render list markers as ordinary
paragraph text even when GitHub displays them as a list.

## API reference

Add or improve Google-style `Args`, `Returns`, `Raises`, and `Examples` sections
beside the implementation. Reference pages explicitly select public objects:

```text
::: yanex.log_metrics
```

Keep examples executable in the documented context. A strict build validates
rendering and links, but does not execute code blocks or prove behavioral claims.

Wrap Python examples in fenced `python` code blocks, including examples in
docstrings. Unfenced `>>>` prompts can render as nested blockquotes. After changing
lists or examples, inspect the rendered page; a successful build alone does not
guarantee the intended layout.

## Shared defaults

The pinned relcon-docs dependency supplies the theme, Markdown exports, equations,
callouts, and diagram colours. API members are alphabetical; underscore-prefixed
members are excluded. Yanex keeps its API source path, heading options, hidden
source blocks and guide/CLI/API export sections in mkdocs.yml.

To upgrade, update the Git pin in pyproject.toml, run `uv lock` and
`uv sync --locked --group docs`, then run `relcon-docs configure --dry-run`,
`relcon-docs configure`, and `relcon-docs configure --check`.
Keep the generated .relcon-docs files, shared CSS and math JavaScript committed;
put local overrides in mkdocs.yml instead of editing managed assets.
Update the reusable deployment workflow pin separately in pages.yml.

## GitHub Pages

The documentation check validates pushes and pull requests without publishing.
The pages.yml workflow publishes on a published GitHub Release or manual dispatch,
using relcon-docs' reusable workflow. Pushes to main do not deploy the site.
For a documentation correction, select **Actions → Documentation → Run workflow**
and choose the reviewed main branch. This publishes docs without a package release.

Set **Settings → Pages → Source** to **GitHub Actions** and allow release tags and the intended manual-dispatch branch in
the github-pages environment. The workflow declares pages and identity-token write
permissions. The published site is https://relaxed-constraints.github.io/yanex/.

Follow [Building and releasing Yanex](releases.md) for release checks and publishing.
The theme's repository badge reflects the latest stable GitHub Release, rather
than identifying the exact deployed commit.
