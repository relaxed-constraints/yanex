# Installation

Yanex requires Python 3.11 or later and Git for recording repository provenance.
Install it in the environment that contains your experiment's dependencies.

<a id="with-uv-recommended"></a>
<a id="with-pip"></a>

## Install Yanex

Include the optional `results` extra if you use pandas analysis or plotting.

=== "uv"

    We recommend [uv](https://docs.astral.sh/uv/getting-started/installation/).
    For a new project, run `uv init my-experiments` and enter that directory first.

    ```bash
    uv add yanex
    # With pandas analysis and plotting:
    uv add 'yanex[results]'
    ```

=== "pip"

    Create and activate a virtual environment for your project if you do not already
    have one. On Windows PowerShell, use `.venv\Scripts\Activate.ps1` to activate it.

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install yanex
    # With pandas analysis and plotting:
    python -m pip install 'yanex[results]'
    ```

## Verify the installation

=== "uv"

    ```bash
    uv run yanex --version
    uv run yanex --help
    ```

=== "pip"

    ```bash
    yanex --version
    yanex --help
    ```

In a uv-managed project, prefix the `yanex` commands in this guide with `uv run`
or activate the project's virtual environment. With pip, run them in the
activated environment where you installed Yanex.

## Experiment dependencies and synchronization

Yanex launches experiment scripts with its Python interpreter, so install your
training or research libraries into that same environment.

SSH synchronization additionally needs `rsync` and working SSH access. S3
synchronization needs the AWS CLI configured for the target bucket.
See [syncing experiments](../user-guide/managing/sync.md).

Continue with [your first experiment](quickstart.md).
