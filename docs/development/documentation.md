# Building and publishing documentation

There is one documentation source tree: `docs/`, organised like the site navigation
in `zensical.toml`. Python API contracts live in source docstrings and are rendered by
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

### Deploy a documentation correction without a package release

1. Edit Markdown or docstrings, preview the affected pages, and run the strict build.
2. Commit the changes, merge them into `main`, and push. The Documentation check
   workflow validates the build but does not deploy it.
3. Open **GitHub → Actions → Documentation → Run workflow** and select `main`
   (or another explicitly reviewed ref). Do not select **Publish to PyPI**.
4. Wait for both build and deploy jobs to succeed. Open the deployment URL from
   the workflow and check the changed pages, code blocks, diagrams, and links.

Manual deployment does not publish to PyPI, create a release, or change a version
number. It replaces the site's contents with the selected ref. After a correction
on `main`, the site can contain changes newer than the latest package release.

### Deploy documentation with a release

Publishing a GitHub Release automatically starts the Documentation workflow for
the tagged source. Ensure that tag contains the intended documentation and workflow
configuration. Follow [Building and releasing Yanex](releases.md) for package
versioning, pre-release checks, PyPI publishing, and post-release verification.

### Understand the version badge

The theme retrieves the latest published GitHub Release from the repository given
by `repo_url`. Bare tags do not populate this badge, and prereleases do not count
as the latest stable release. The badge is not a record of the deployed commit:
a manual deployment can show newer documentation beside an older release number.

If it is missing, first check that the repository has a published stable release
and that `repo_url` is correct. Browser/network restrictions or GitHub API limits
can also prevent fetching repository information. Do not hardcode a version in
`repo_name` to work around a missing release.

### Troubleshoot deployment

Check **Settings → Pages** and the workflow's build/deploy logs. Pages must use
GitHub Actions as its source, the `github-pages` environment must allow the
selected branch or tag, and the deploy job needs `pages: write` and
`id-token: write`. These permissions are already declared in `pages.yml`.

If the build fails on a link or API object, fix the source and rerun the strict
build locally. If deployment fails after a successful build, inspect the Pages
configuration before changing documentation content. Rerun a transient failure;
for a content fix, commit the correction and dispatch the updated ref.
