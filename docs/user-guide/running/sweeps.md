# Sweeps, parallel execution, and staging

Yanex supports parameter sweeps to run multiple experiments with different configurations. You can execute sweeps immediately or stage them for later execution.

## Direct Sweep Execution

Run parameter sweeps immediately without staging:

```bash
# Run sweep sequentially (one after another)
yanex run script.py --param "workload_size=list(50, 100, 200)"

# Run sweep in parallel with 4 workers
yanex run script.py --param "workload_size=list(50, 100, 200)" --parallel 4

# Auto-detect CPU count for parallel execution
yanex run script.py --param "learning_rate=logspace(-4, -1, 10)" --parallel 0
```

## Sweep Syntax

The following sweep syntax is supported in both CLI parameters and config files:

- `value1,value2,value3` - Comma-separated alternatives
- `list(value1, value2, ...)` - Explicit alternative list
- `range(stop)`, `range(start, stop)`, `range(start, stop, step)` - Stop-exclusive range
- `linspace(start, end, num)` - Generates evenly spaced values
- `logspace(start_exp, end_exp, num)` - Generates logarithmically spaced values

A YAML list or JSON list such as `[16, 32, 64]` is a single parameter value.
Use a sweep expression when you want separate runs. Preview expansion and rendered
metadata with `--dry-run` before launching a large grid.

**CLI Examples:**

```bash
# List of specific values
--param "batch_size=list(16, 32, 64, 128)"

# Range: generates [4, 5, 6, 7]
--param "workload_size=range(4, 8, 1)"

# Linspace: generates 5 evenly spaced values from 10 to 100
--param "n_nodes=linspace(10, 100, 5)"

# Logspace: generates [0.0001, 0.001, 0.01, 0.1]
--param "learning_rate=logspace(-4, -1, 4)"
```

**Config File Examples:**

```yaml
# config.yaml
# Define sweeps directly in configuration files
learning_rate: "list(0.001, 0.01, 0.1)"
batch_size: "list(32, 64, 128)"
dropout: "linspace(0.1, 0.5, 5)"
warmup_steps: "range(0, 1000, 200)"
```

```bash
# Run config file sweep
yanex run script.py --config config.yaml

# Run in parallel with 4 workers
yanex run script.py --config config.yaml --parallel 4
```

**Note:** Whitespace in sweep syntax is flexible (e.g., `list(1,2,3)` equals `list(1, 2, 3)`)

## Grid Search (Multi-Parameter Sweeps)

If multiple parameter sweeps are defined (via CLI or config file), Yanex performs a grid search across all combinations:

**CLI Grid Search:**

```bash
# Sequential execution of 9 experiments (3 × 3)
yanex run script.py \
  --param "learning_rate=list(0.001, 0.01, 0.1)" \
  --param "batch_size=list(32, 64, 128)"

# Parallel execution with 4 workers
yanex run script.py \
  --param "learning_rate=list(0.001, 0.01, 0.1)" \
  --param "batch_size=list(32, 64, 128)" \
  --parallel 4
```

**Config File Grid Search:**

```yaml
# config.yaml
# Creates 9 experiments (3 × 3)
learning_rate: "list(0.001, 0.01, 0.1)"
batch_size: "list(32, 64, 128)"
epochs: 100  # Regular parameter (not swept)
```

```bash
# Run grid search from config
yanex run script.py --config config.yaml --parallel 4
```

This creates and runs 9 experiments with all combinations of the two swept parameters.

## Staged Sweep Execution

You can still stage experiments for later execution:

```bash
# Stage parameter sweep
yanex run script.py --param "workload_size=list(50, 100, 200)" --stage

# Run all staged experiments sequentially
yanex run --staged

# Run all staged experiments in parallel with 4 workers
yanex run --staged --parallel 4
```

**When to use staging:**

- Preparing multiple experiment batches before execution
- Running experiments at a later time (e.g., overnight)
- Reviewing experiment configurations before execution

## Parallel Execution

The `--parallel` flag enables parallel execution using multiple workers:

```bash
# Specify worker count
yanex run script.py --param "lr=logspace(-4, -1, 10)" --parallel 4

# Auto-detect CPU count (uses all available cores)
yanex run script.py --param "lr=logspace(-4, -1, 10)" --parallel 0

# Short flag syntax (like make -j)
yanex run script.py --param "lr=logspace(-4, -1, 10)" -j 4
```

**Benefits:**

- True parallelism using separate processes (bypasses Python GIL)
- Each experiment runs in isolation with separate storage
- Progress tracking with completion summary
- Ideal for multi-core systems and hyperparameter tuning
- Independent `yanex run` commands from different shells can run concurrently

**Usage Notes:**

- `--parallel` flag is for throttling managed execution (sweeps and staged experiments)
- Cannot be combined with `--stage` (stage first, then run with `--parallel`)
- For running multiple independent experiments concurrently, simply run `yanex run` from different shells - no special flags needed

## Staging Experiments

Yanex allows you to stage experiments before running them, which is useful for preparing batches of experiments or reviewing configurations before execution.

```bash
# Stage a single experiment
yanex run script.py --stage

# Stage parameter sweeps
yanex run script.py --param "lr=list(0.01, 0.001)" --stage
```

### Run Staged Experiments

```bash
# Run all staged experiments sequentially
yanex run --staged

# Run all staged experiments in parallel
yanex run --staged --parallel 4
```
