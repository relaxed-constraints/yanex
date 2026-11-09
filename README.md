# Yanex

**Yet Another Experiment Tracker** — lightweight, Git-aware experiment tracking for Python.

[![PyPI version](https://img.shields.io/pypi/v/yanex)](https://pypi.org/project/yanex/)
[![Python versions](https://img.shields.io/pypi/pyversions/yanex)](https://pypi.org/project/yanex/)
[![License](https://img.shields.io/pypi/l/yanex)](https://github.com/relaxed-constraints/yanex/blob/main/LICENSE)

[Documentation](https://relaxed-constraints.github.io/yanex/) ·
[Getting started](https://relaxed-constraints.github.io/yanex/getting-started/quickstart/) ·
[Examples](https://relaxed-constraints.github.io/yanex/examples/) ·
[Releases](https://github.com/relaxed-constraints/yanex/releases)

Keep parameters, metrics, artifacts, and code provenance together for benchmarks,
simulations, data processing, and machine learning. Yanex stores experiments as
local files and does not require a tracking server. Run ordinary Python scripts,
compare results, and connect experiments into reproducible research workflows.

## What Yanex provides

- **Experiment records:** Capture configuration, logged metrics and artifacts,
  stdout/stderr, environment information, and Git metadata when available.
- **Configuration and sweeps:** Use YAML files, command-line overrides, parameter
  sweeps, parallel execution, and staging for later runs.
- **Dependencies and artifact reuse:** Connect experiments by ID into directed
  acyclic graphs, with named dependency slots, dependency sweeps, and fan-in runs.
- **Results analysis:** Find and compare runs in the terminal, export results, or
  analyze them through the Python API with pandas and plotting support.
- **Organisation and automation:** Use names, tags, projects, metadata templates,
  machine-readable output, and experiment syncing over SSH or S3.
- **Web interface (beta):** Browse experiments and their dependency graphs in a
  local web UI. This interface is still under development.

Git tracking helps preserve code provenance; it does not guarantee reproducibility
on its own. See [Git tracking and reproducibility](https://relaxed-constraints.github.io/yanex/user-guide/managing/reproducibility/)
for what is captured and its limitations.

## Installation

Yanex requires **Python 3.11 or later**. We recommend
[uv](https://docs.astral.sh/uv/) for managing your project and its environment.
In an existing uv project:

```bash
uv add yanex
```

For a new project, run `uv init my-experiments` and `cd my-experiments` first.
For pandas analysis and plotting, use `uv add 'yanex[results]'`.

Alternatively, install with pip in an activated virtual environment:

```bash
pip install yanex
```

The commands below use `uv run`. If you installed with pip, run `yanex` directly
in your activated environment. See the
[installation guide](https://relaxed-constraints.github.io/yanex/getting-started/installation/)
for optional dependencies and setup details.

## Quickstart

Save this as `benchmark.py`. It measures a small computation, logs its duration,
and saves the result as a JSON artifact:

```python
from time import perf_counter

import yanex

samples = yanex.get_param("samples", default=100_000)

start = perf_counter()
result = sum(i * i for i in range(samples))
elapsed = perf_counter() - start

yanex.log_metrics({"elapsed_seconds": elapsed})
yanex.save_artifact({"samples": samples, "result": result}, "result.json")
```

Run it with tracking, then explore the recorded experiment:

```bash
uv run yanex run benchmark.py --param samples=200000 --name baseline --tag benchmark
uv run yanex list
uv run yanex show baseline
```

Each run gets a unique ID and its own directory under `~/.yanex/experiments/` by
default. In a Git repository, listing and filtering commands default to the current
project. Direct ID lookups work across projects. Names can be reused; use an ID
when a name matches more than one run.

The script also works standalone with `uv run python benchmark.py`.
[Standalone execution](https://relaxed-constraints.github.io/yanex/getting-started/execution-patterns/)
uses parameter defaults and does not create a tracked experiment.

### Run a sweep and compare results

Run the same script with three input sizes, using up to three workers:

```bash
uv run yanex run benchmark.py --param "samples=100000,200000,400000" \
  --parallel 3 --tag benchmark-sweep

uv run yanex compare --tag benchmark-sweep
uv run yanex compare --tag benchmark-sweep --format csv > results.csv
```

Sweeps also support ranges and linear or logarithmic spacing. Multiple swept
parameters produce a Cartesian product. Parallel runs share machine resources,
so use sequential runs when contention would distort a timing comparison.
See [sweeps, parallel execution, and staging](https://relaxed-constraints.github.io/yanex/user-guide/running/sweeps/).

### Read results from scripts and tools

Use `yanex get` to retrieve individual fields, or export experiment metadata as
JSON. Replace `EXPERIMENT_ID` with an ID from `yanex list`:

```bash
uv run yanex get param:samples EXPERIMENT_ID
uv run yanex get metric:elapsed_seconds EXPERIMENT_ID
uv run yanex list --tag benchmark-sweep --format json
```

For analysis in Python, install the `results` extra and use the Results API:

```python
import yanex.results as yr

df = yr.compare(
    tags=["benchmark-sweep"],
    params=["samples"],
    metrics=["elapsed_seconds"],
)
print(df)
```

The Results API does not automatically limit queries to the current Git project;
add `project="my-experiments"` when you want that scope.

## Documentation

The [documentation site](https://relaxed-constraints.github.io/yanex/) contains
setup instructions, detailed workflows, and the complete CLI and Python API references.

| Topic | Guide |
| --- | --- |
| Parameters and configuration files | [Configuration](https://relaxed-constraints.github.io/yanex/user-guide/running/configuration/) |
| Logging results and saving files | [Metrics and artifacts](https://relaxed-constraints.github.io/yanex/user-guide/running/metrics-artifacts/) |
| Existing shell scripts and external tools | [Running Bash scripts](https://relaxed-constraints.github.io/yanex/user-guide/running/bash-scripts/) |
| Pipelines and shared artifacts | [Experiment dependencies](https://relaxed-constraints.github.io/yanex/user-guide/pipelines/dependencies/) |
| Command-line usage | [CLI reference](https://relaxed-constraints.github.io/yanex/cli/) |
| Instrumentation and programmatic execution | [Run API](https://relaxed-constraints.github.io/yanex/api/run/) |
| Post-hoc analysis and comparison | [Results API](https://relaxed-constraints.github.io/yanex/api/results/) |
| Machine-readable output and the Claude Code skill | [AI and automation](https://relaxed-constraints.github.io/yanex/user-guide/automation/) |
| Runnable scripts and notebooks | [Examples](https://relaxed-constraints.github.io/yanex/examples/) |

## Contributing

Contributions and bug reports are welcome. Start with the
[contributing guide](https://relaxed-constraints.github.io/yanex/development/contributing/)
and [testing guide](https://relaxed-constraints.github.io/yanex/development/testing/).
Maintainers can follow the [build and release guide](https://relaxed-constraints.github.io/yanex/development/releases/)
for package builds, PyPI publication, and documentation deployment.

Report bugs and propose features through
[GitHub Issues](https://github.com/relaxed-constraints/yanex/issues).

## Acknowledgements

Yanex is inspired by the original [Guild AI experiment-tracking toolkit](https://github.com/guildai/guildai).
Its command-line workflow and local, file-based experiment records were a major
influence on Yanex. Thank you to its creators and contributors for a tool that
made research workflows simpler.

The [original documentation](https://guildai.org/t/guild-ai-documentation/64)
is still available. For more background on the project's direction, see
[the maintainer's update](https://github.com/guildai/guildai/discussions/523).

## License

Yanex is released under the [MIT License](https://github.com/relaxed-constraints/yanex/blob/main/LICENSE).
