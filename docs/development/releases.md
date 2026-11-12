# Building and releasing Yanex

Yanex uses the same release-driven publishing approach as BONDI. A published
GitHub Release starts the PyPI workflow and the documentation deployment. Pushing
to `main` or pushing a tag alone does not publish a package or deploy the docs.

## Workflow overview

| Workflow | Trigger | What it does |
| --- | --- | --- |
| Release checks (`release-checks.yml`) | Manual dispatch or called by the release workflow | Tests Python 3.11/3.12, checks formatting and docs, builds and tests the frontend, builds and validates distributions |
| Publish to PyPI (`release.yml`) | GitHub Release published | Checks tag/version agreement, runs Release checks, publishes the resulting distributions using Trusted Publishing |
| Documentation check (`docs.yml`) | Push, pull request, or manual dispatch | Builds documentation strictly without deploying |
| Documentation (`pages.yml`) | GitHub Release published or manual dispatch | Builds and deploys the selected source to GitHub Pages |
| Web UI (`web-ui.yml`) | Push or pull request changing frontend files or its workflow | Runs frontend tests, type checks, and a production build |

The PyPI and Pages workflows run independently. A successful documentation
deployment does not prove that the PyPI release succeeded, or vice versa.

## Local environment

Run the commands on this page from the repository root unless noted otherwise.
Install Git, uv, and Node.js 22 with npm. GitHub Actions uses Python 3.11 for
package builds and tests both Python 3.11 and 3.12.

```bash
git clone https://github.com/relaxed-constraints/yanex.git
cd yanex
uv sync --locked --all-extras --dev --group docs
npm --prefix yanex/web ci
```

`uv.lock` pins Python dependencies and `yanex/web/package-lock.json` pins frontend
dependencies. Commit intentional dependency changes with their lockfiles.
The Node.js version selected for frontend builds is separate from the internal
Node.js runtime used by GitHub Actions themselves.

## Prepare the version and changelog

Use a feature branch and merge the reviewed release changes into `main` before
creating the release tag.

1. Choose a new, unused package version.
2. Update `[project].version` in `pyproject.toml`. This is the authoritative version;
   runtime and CLI version strings read package metadata through `yanex._version`.
3. Move the appropriate entries from `Unreleased` in `CHANGELOG.md` into a dated
   section for the new version. Describe user-visible changes and migration steps.
4. Update the user guide, CLI reference, API docstrings, and examples where needed.
5. Refresh the lockfile and installed metadata, then check the reported version:

```bash
uv lock
uv sync --locked --all-extras --dev --group docs
uv run yanex --version
```

The legacy `setup.py` and the private frontend package's version are not the
release version source. Do not create a new tag until the package version,
changelog, and built distributions agree.

## Run local checks

```bash
uv run ruff check --fix
uv run ruff format
uv run ruff check
uv run pytest --cov=yanex --cov-report=term-missing --cov-fail-under=80 -n 0
uv run --group docs zensical build --strict
npm --prefix yanex/web run test
npm --prefix yanex/web run typecheck
npm --prefix yanex/web run build
```

The release coverage gate is temporarily **80%**. Keep it aligned with
`release-checks.yml`; increasing coverage remains a development goal. Tests run
sequentially in release CI. For quicker local iteration, the ordinary
`uv run pytest` command uses parallel workers by default.

Use isolated experiment stores for executable documentation probes. Tag probes
so they can be identified, and remove only the data created for those checks.
See [Testing](testing.md) for isolation fixtures.

## Build and inspect the distributions

Build the frontend before building the Python package: the wheel and source
archive include `yanex/web/out/`, and `uv build` does not compile the frontend.

```bash
npm --prefix yanex/web ci
npm --prefix yanex/web run build
rm -rf dist/
uv build
uvx --from twine twine check --strict dist/*
```

`dist/` should contain one wheel and one source archive for the intended version.
Clearing old distributions prevents accidentally uploading a previous build.
Do not use a stale `out/` directory as evidence that the current frontend builds.

Install the wheel into a fresh environment and test it outside the checkout:

```bash
release_check_dir=$(mktemp -d)
uv venv "$release_check_dir/venv"
uv pip install --python "$release_check_dir/venv/bin/python" dist/*.whl
(
    cd "$release_check_dir"
    ./venv/bin/yanex --version
    ./venv/bin/yanex --help
    ./venv/bin/python -c "from pathlib import Path; import yanex; assert (Path(yanex.__file__).parent / 'web' / 'out' / 'index.html').is_file()"
)
```

Also smoke-test the CLI, the web interface, and any APIs changed by the release.
Install the `results` extra when checking plotting or analysis features. The
release workflow checks wheel installation and the bundled web UI automatically;
feature-specific smoke tests are the maintainer's responsibility.

## Configure PyPI Trusted Publishing

This is one-time setup for the repository/workflow identity. Changing the owner,
repository, workflow filename, or environment requires updating the publisher.

In **PyPI → Your projects → yanex → Manage → Publishing**, add a GitHub trusted
publisher with these exact values:

| Field | Value |
| --- | --- |
| Owner | `relaxed-constraints` |
| Repository | `yanex` |
| Workflow filename | `release.yml` |
| Environment | `pypi` |

In **GitHub → Settings → Environments**, create the `pypi` environment. If you
restrict deployment branches or tags, allow the intended `v*` release tags.
Optional required reviewers can provide a final publication approval.

The publish job requests a short-lived credential through GitHub's OIDC identity.
It does not read `PYPI_TOKEN`. Keep any existing token until the first trusted
publication is verified, then remove it if no other publishing process uses it.
See the [PyPI setup instructions](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).

## Validate in GitHub before publishing

After merging and pushing the intended changes, open **Actions → Release checks →
Run workflow**, choose `main`, and wait for all jobs to pass. This builds packages
but does not publish to PyPI or deploy documentation.

The checks run Python tests on both supported CI versions, Ruff, the strict docs
build, frontend tests/type checks/build, distribution checks, and an installed-wheel
check. The resulting `distributions` artifact contains the wheel and source archive.
Review failures and ensure `main` has not changed since the successful check before
tagging the intended commit.

## Publish a new version

Once checks pass, create an annotated tag at the reviewed commit. Replace
`0.X.Y` below with the package version and `REVIEWED_COMMIT` with its commit hash:

```bash
git fetch origin
git tag -a v0.X.Y REVIEWED_COMMIT -m "Yanex 0.X.Y"
git push origin v0.X.Y
```

In **GitHub → Releases → Draft a new release**, choose that existing tag, add the
release notes, and publish. A stable release should not be marked as a prerelease.

Publishing starts:

1. **Publish to PyPI:** validates that the tag is exactly `v` plus the version in
   `pyproject.toml`, runs the checks, and uploads their exact distributions. The
   publish job does not rebuild the packages.
2. **Documentation:** builds the tagged documentation and deploys GitHub Pages.

Use a new version for each PyPI release. Do not move an already published tag or
attempt to replace uploaded distributions. Do not publish a historical tag merely
to populate the documentation badge: the tagged source controls which workflows
and package contents are used.

## Verify the release

Check both workflows separately, then verify:

- The new version, release notes, and source tag on GitHub.
- The expected version and wheel/source files on the
  [PyPI project page](https://pypi.org/project/yanex/).
- A fresh installation from PyPI, outside the source checkout:

```bash
published_check_dir=$(mktemp -d)
uv venv "$published_check_dir/venv"
uv pip install --python "$published_check_dir/venv/bin/python" 'yanex[results]==0.X.Y'
(
    cd "$published_check_dir"
    ./venv/bin/yanex --version
    ./venv/bin/yanex --help
)
```

Open the [published documentation](https://relaxed-constraints.github.io/yanex/)
and inspect the pages affected by the release, API examples, and navigation links.
See [Documentation publishing](documentation.md#github-pages) for manual corrections.

## Recover from a failed workflow

Inspect the failed job before retrying. A failed Python check should not be bypassed
by uploading distributions manually.

| Failure | What to check |
| --- | --- |
| Tag/version mismatch | The tagged `pyproject.toml` must match the release tag exactly |
| Tests or coverage | Reproduce the failing test and the 80% coverage gate locally |
| Missing web UI in the wheel | Ensure the frontend built successfully before the Python build |
| Trusted publisher rejection | Match owner, repository, `release.yml`, and `pypi` exactly on PyPI; check the GitHub environment rules |
| PyPI file already exists | Inspect what uploaded successfully; do not overwrite or casually rerun a partial publication |
| Pages deployment failed | Check Pages source, `github-pages` environment rules, and the Documentation workflow logs |

For transient failures with no uploads, GitHub's rerun controls can retry the same
reviewed commit. If fixing source or workflow code requires a new commit, validate
that commit and make a new release version rather than moving a published tag.
For partial PyPI uploads, inspect the files already present before choosing a
recovery; rerunning the default publisher may reject duplicates.
