# `yanex run` - Execute Tracked Experiments

Run Python scripts as tracked experiments with automatic parameter management, Git integration, and result logging.

## Quick Start

```bash
# Basic experiment
yanex run my_script.py

# With configuration file
yanex run my_script.py --config config.yaml

# With parameter overrides
yanex run my_script.py --param learning_rate=0.01 --param epochs=100

# With metadata
yanex run my_script.py --name "baseline-model" --tag production
```

## Overview

The `yanex run` command is the core of Yanex - it executes your Python scripts while automatically tracking:

- **Parameters**: From config files and CLI overrides
- **Git State**: Current commit, branch, and working directory status
- **Results**: Via `yanex.log_metrics()` calls in your script
- **Artifacts**: Files saved during execution (e.g. model checkpoints, logs)
- **Metadata**: Experiment name, description, tags, timing

For each experiment run, Yanex assigns a unique ID and creates a dedicated directory to store all related data (defaults to `~/.yanex/experiments/<id>`).

Yanex logs stdout and stderr outputs, all logged artifact files, logged results, the config file with all parameters used (including overrides), and metadata like the start time, end time and duration of your experiments, the git state of your repository at the time of execution, name, description, and tags.

These records support reproducibility and comparison of results.


## Command Options

### Required Arguments

- `script_path`: Path to Python script to execute (omit when using `--staged`)

### Optional Arguments

#### Parameter Overrides

- `--param KEY=VALUE`: Override configuration parameter
- `--config PATH` / `-c PATH`: Use configuration file (can be repeated for multiple files)
- `--clone-from EXP_ID`: Clone configuration from another experiment

#### Dependencies

- `--depends-on SLOT=EXP_ID` / `-D SLOT=EXP_ID`: Bind a dependency slot. Repeat for multiple inputs; comma-separated IDs within a slot create a dependency sweep. Bare IDs receive automatic slot names.

#### Metadata

- `--name NAME`: Set experiment name
- `--description DESC`: Set experiment description
- `--tag TAG`: Add tag (can be used multiple times)
- `--project PROJECT`: Set project name (default: auto-detected from git repo name; can also be set via `yanex.project` in config)

#### Git Options

- `--ignore-dirty`: *(Deprecated)* This flag is no longer needed and will be removed in a future version

#### Staging

- `--stage`: Stage the experiment for later execution
- `--staged`: Run all staged experiments

#### Parallel Execution

- `--parallel N` / `-j N`: Run experiments in parallel with N workers (0=auto-detect CPUs)

#### General Options

- `--dry-run`: Validate parameters without executing the script
- `--help`: Show help message and exit



## Basic Usage

### Simple Execution

```bash
yanex run script.py
```

Runs `script.py` with default configuration (loads `./config.yaml` if present).

### With Parameters

```bash
# Override single parameter
yanex run script.py --param learning_rate=0.01

# Override multiple parameters
yanex run script.py --param learning_rate=0.01 --param batch_size=64 --param epochs=200
```

### With Metadata

```bash
yanex run script.py \
  --name "baseline-experiment" \
  --description "Initial training run with default hyperparameters" \
  --tag baseline \
  --tag production
```

## Workflow guides

- [Configuration](../user-guide/running/configuration.md)
- [Sweeps, parallel execution, and staging](../user-guide/running/sweeps.md)
- [Dependencies](../user-guide/pipelines/dependencies.md)
- [Git tracking and cloning](../user-guide/managing/reproducibility.md)
- [Metadata templates](../user-guide/running/metadata.md)
