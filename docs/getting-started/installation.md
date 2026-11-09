# Installation

Yanex requires Python 3.11 or later and Git for recording repository provenance.
Install it in the environment that contains your experiment's dependencies.

## With uv (recommended)

We recommend [uv](https://docs.astral.sh/uv/) for managing your Python project,
dependencies, and virtual environment. If you do not have it installed, follow
[uv's installation instructions](https://docs.astral.sh/uv/getting-started/installation/).

In an existing uv project, add Yanex:

```bash
uv add yanex
```

For a new project, run `uv init my-experiments` and `cd my-experiments` first.
For pandas analysis and plotting, include the optional results dependencies:

```bash
uv add 'yanex[results]'
```

Run Yanex in the project's environment:

```bash
uv run yanex --version
uv run yanex --help
uv run yanex run experiment.py
```

Throughout this documentation, prefix `yanex` commands with `uv run` when using a
uv-managed project, or activate its virtual environment first.

If you prefer to manage a virtual environment directly, uv also provides
`uv venv` and `uv pip install yanex`. See
[uv's environment guide](https://docs.astral.sh/uv/pip/environments/).

## With pip

In your activated virtual environment:

```bash
pip install yanex
```

For pandas analysis and plotting:

```bash
pip install 'yanex[results]'
```

Check the installation with `yanex --version` and `yanex --help`.

## Experiment dependencies and synchronization

Yanex launches experiment scripts with its Python interpreter, so install your
training or research libraries into that same environment.

SSH synchronization additionally needs `rsync` and working SSH access. S3
synchronization needs the AWS CLI configured for the target bucket.
See [syncing experiments](../user-guide/managing/sync.md).

Continue with [your first experiment](quickstart.md).
