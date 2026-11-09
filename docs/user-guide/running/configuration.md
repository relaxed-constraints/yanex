# Configuration Guide

Complete guide to parameter management and configuration in Yanex.

## Quick Start

```yaml
# config.yaml
learning_rate: 0.001
batch_size: 32
epochs: 100
model_type: "transformer"
```

```bash
# Override parameters at runtime
yanex run train.py --config config.yaml --param learning_rate=0.01 --param epochs=50
```

## Configuration Files

### Basic Structure

Yanex uses YAML configuration files for default parameters:

```yaml
# config.yaml
# Model parameters
model:
  learning_rate: 0.001
  batch_size: 32
  num_layers: 12
  dropout: 0.1

# Training parameters
training:
  epochs: 100
  optimizer: "adam"
  scheduler: "cosine"
  early_stopping: 10

# Data parameters
data:
  dataset: "cifar10"
  validation_split: 0.2
  augmentation: true
```

### Multiple Configuration Files

Yanex supports loading multiple configuration files that are merged together, allowing you to organize your configuration into modular, reusable pieces. When multiple config files are provided, they are merged in order from left to right, with later files taking precedence over earlier ones.

**Example Setup:**

```yaml
# data-config.yaml
data:
  filename: "my-data.jsonl"
  split: 0.2
```

```yaml
# model-config.yaml
model:
  epochs: 1000
  learning_rate: 0.01
```

```yaml
# metadata-config.yaml
yanex:
  name: training
  tag: [study, baseline]
```

**Usage:**

```bash
# Load and merge multiple config files
yanex run train.py --config data-config.yaml --config model-config.yaml --config metadata-config.yaml

# All configs are merged into a single configuration
# Experiment parameters contain data and model; yanex supplies CLI defaults
```

**Benefits:**

- **Modularity:** Separate data, model, and infrastructure configurations
- **Reusability:** Swap out individual config files while keeping others the same
- **Environment-specific:** Easily switch between dev/staging/production configs
- **Merge Order:** Later configs override earlier ones for conflicting keys

**Merge Example:**

```yaml
# base-config.yaml
learning_rate: 0.01
batch_size: 32
epochs: 100
```

```yaml
# override-config.yaml
learning_rate: 0.001  # Overrides base-config value
optimizer: "adam"     # New parameter
```

```bash
yanex run train.py --config base-config.yaml --config override-config.yaml
# Result: learning_rate=0.001, batch_size=32, epochs=100, optimizer="adam"
```

### Accessing Configuration

```python
import yanex

# Load configuration as a dictionary
params = yanex.get_params()

# Load individual parameters (with defaults)
lr = yanex.get_param('learning_rate', default=0.001)
batch_size = yanex.get_param('batch_size', default=32)
```

## Parameter Hierarchy

Explicit CLI parameter overrides take precedence over YAML values. Multiple config
files merge left to right; later files win. Code-level defaults in `get_param()`
apply when the requested key is absent. Without `--config`, Yanex looks for
`config.yaml` in the invocation working directory.

The reserved `yanex` section supplies CLI metadata defaults rather than ordinary
experiment parameters. Explicit CLI options override those defaults.

## CLI Parameter Overrides

### Basic Syntax

```bash
# Single parameter
yanex run script.py --param learning_rate=0.01

# Multiple parameters
yanex run script.py --param learning_rate=0.01 --param epochs=200 --param batch_size=64
```

### Nested Parameters

```bash
# Nested structure access with dot notation
yanex run script.py --param model.learning_rate=0.01
yanex run script.py --param training.optimizer=sgd
yanex run script.py --param data.validation_split=0.3
```

### Parameter Types

```bash
# Numbers
--param learning_rate=0.001      # Float
--param learning_rate=1e-4       # Scientific notation: 0.0001
--param epochs=100               # Integer

# Strings
--param model_type=transformer   # String
--param optimizer=adam           # String

# Booleans
--param use_dropout=true         # Boolean
--param debug=false              # Boolean

# Lists (JSON format)
--param "layers=[64,128,256]"      # List of integers
--param "tags=[\"exp\",\"test\"]"  # List of strings (note: requires escaping)
```

### Scientific Notation

Scientific notation is supported in CLI parameters and YAML configuration files.
For example, `1e-4` is parsed as the floating-point value `0.0001`:

```bash
yanex run train.py --param learning_rate=1e-4
```

```yaml
learning_rate: 1e-4
```

In both cases, `yanex.get_param("learning_rate")` returns a Python `float`.

### Parameter Sweeps

Use comma-separated values or `range()`, `linspace()`, and `logspace()` expressions
to expand configurations into multiple experiments. A YAML list or JSON list value
is a single list-valued parameter, not a sweep.

See [sweeps, parallel execution, and staging](sweeps.md) for syntax, YAML examples,
and execution options.

## CLI Defaults from Config

You can set default values for `yanex run` CLI arguments directly in your configuration file using a special `yanex` section. This allows you to avoid repeating common CLI options while still allowing them to be overridden when needed.

### Setting CLI Defaults

```yaml
# config.yaml
# Your experiment parameters
learning_rate: 0.001
batch_size: 32
epochs: 100

# CLI defaults for yanex run command
yanex:
  name: "transformer-experiment"
  tag: ["ml", "transformer", "dev"]
  description: "Training transformer model on text data"
  dry_run: false
  stage: false
```

### CLI Override Precedence

CLI arguments still override config defaults, maintaining expected precedence:

```bash
# Uses name from config ("transformer-experiment")
yanex run train.py --config config.yaml

# Overrides name from config
yanex run train.py --config config.yaml --name "custom-experiment"

# Uses tags from config but overrides name
yanex run train.py --config config.yaml --name "override" --tag production
```

### Supported CLI Parameters

The `yanex` section supports these `yanex run` parameters:

- `name`: Experiment name
- `tag`: Tags (single string or list)
- `description`: Experiment description
- `dry_run`: Dry run mode (boolean)
- `stage`: Stage changes before run (boolean)
- `project`: Project name (overrides auto-detection from git repo name)

**Note:** This feature only works with the `yanex run` command - other commands like `list`, `show`, etc. are not affected.

### Project Name

Yanex automatically detects the project name from your git repository name and stores it in experiment metadata. You can override this with the `yanex.project` key in your config file:

```yaml
# config.yaml
learning_rate: 0.001
batch_size: 32

yanex:
  project: my-custom-name
```

Or via the CLI:

```bash
yanex run train.py --project my-custom-name
```

The project name is used for filtering experiments. By default, `yanex list` and other query commands only show experiments from the current project. Use `--global` to see all experiments across projects.

### Git Integration

Yanex captures changes to tracked files as Git patches; untracked files and notebook changes must be preserved separately. Each experiment stores:

- The current commit hash
- Branch name
- Uncommitted changes (saved as `artifacts/git_diff.patch`)

See [Best Practices - Git Workflow](../best-practices.md#git-workflow-integration) for details.

## Environment Variables

`YANEX_EXPERIMENTS_DIR` selects the experiment store. Set it before launching
Yanex or importing and using the Python APIs.

`YANEX_EXPERIMENT_ID`, `YANEX_CLI_ACTIVE`, `YANEX_CLI_ARGS`, and `YANEX_PARAM_*`
carry context into child processes. They are implementation transport variables,
not a substitute for recorded configuration. Use YAML or `--param` for experiment
inputs so that stored parameters agree with what your script receives. Double
underscores in environment-variable names do not provide nested-key expansion.

### Environment-Specific Configs

```yaml
# base_config.yaml
model:
  architecture: "resnet"
  layers: 18

training:
  epochs: 100
  optimizer: "adam"
```

```yaml
# production.yaml
model:
  layers: 50  # Override base config

training:
  epochs: 200
  batch_size: 128
```

```bash
# Production run
yanex run train.py --config base_config.yaml --config production.yaml
```

## Advanced Configuration

### Complex Data Types

```yaml
# config.yaml
model:
  # Lists
  layer_sizes: [64, 128, 256, 512]
  dropout_rates: [0.1, 0.2, 0.3, 0.4]

  # Nested objects
  optimizer:
    type: "adam"
    params:
      lr: 0.001
      weight_decay: 0.0001
      betas: [0.9, 0.999]

  # Mixed types
  features:
    - name: "conv1"
      filters: 64
      kernel_size: 3
    - name: "conv2"
      filters: 128
      kernel_size: 3

# Boolean and null values
training:
  use_gpu: true
  checkpoint_path: null  # Explicitly null
  mixed_precision: false
```

### Accessing Complex Types

```python
params = yanex.get_params()

# Lists
layer_sizes = params['model']['layer_sizes']  # [64, 128, 256, 512]
first_layer = layer_sizes[0]  # 64

# Nested objects
optimizer_lr = params['model']['optimizer']['params']['lr']  # 0.001

# Mixed structures
conv_layers = params['model']['features']
first_conv_filters = conv_layers[0]['filters']  # 64
```

## Configuration Validation

### Parameter Validation in Scripts

```python
import yanex

def validate_params(params):
    """Validate experiment parameters."""
    required_keys = ['learning_rate', 'batch_size', 'epochs']

    for key in required_keys:
        if key not in params:
            raise ValueError(f"Missing required parameter: {key}")

    if params['learning_rate'] <= 0:
        raise ValueError("Learning rate must be positive")

    if params['batch_size'] not in [16, 32, 64, 128]:
        raise ValueError("Batch size must be one of: 16, 32, 64, 128")

def main():
    params = yanex.get_params()
    validate_params(params)

    # Your experiment code

```

### Default Values Pattern

```python
def get_model_config(params):
    """Get model configuration with sensible defaults."""
    model_params = params.get('model', {})

    return {
        'learning_rate': model_params.get('learning_rate', 0.001),
        'batch_size': model_params.get('batch_size', 32),
        'num_layers': model_params.get('num_layers', 6),
        'dropout': model_params.get('dropout', 0.1),
        'activation': model_params.get('activation', 'relu')
    }
```

## Best Practices

### 1. Organize Configuration Hierarchically

```yaml
# Good: Organized by component
model:
  architecture: "transformer"
  num_layers: 12
  hidden_size: 768

training:
  learning_rate: 0.001
  batch_size: 32
  epochs: 100

data:
  dataset: "wikitext"
  seq_length: 512
  vocab_size: 50000
```

```yaml
# Avoid: Flat structure for complex configs
learning_rate: 0.001
batch_size: 32
num_layers: 12
hidden_size: 768
dataset: "wikitext"
seq_length: 512
# ... becomes hard to manage
```

### 2. Document Parameters

```yaml
# config.yaml with documentation
model:
  learning_rate: 0.001    # Initial learning rate for Adam optimizer
  batch_size: 32         # Training batch size (memory dependent)
  num_layers: 12         # Number of transformer layers
  dropout: 0.1           # Dropout probability for regularization

training:
  epochs: 100            # Maximum training epochs
  early_stopping: 10     # Stop if no improvement for N epochs
  gradient_clip: 1.0     # Gradient clipping threshold
```

### 3. Use Environment-Specific Configs

```bash
# Directory structure
configs/
├── base.yaml           # Common parameters
├── development.yaml    # Dev-specific overrides
├── staging.yaml        # Staging overrides
└── production.yaml     # Production overrides
```

```bash
# Environment-specific runs
yanex run train.py --config configs/base.yaml --config configs/development.yaml
yanex run train.py --config configs/base.yaml --config configs/production.yaml
```

### 4. Validate Critical Parameters

```python
def main():
    params = experiment.get_params()

    # Validate critical parameters early
    assert params['learning_rate'] > 0, "Learning rate must be positive"
    assert params['batch_size'] > 0, "Batch size must be positive"
    assert params['epochs'] > 0, "Epochs must be positive"

    # Your experiment code
```


## Troubleshooting

### Common Issues

**Parameter not found:**
```python
# Problem: KeyError when accessing nested parameter
lr = params['model']['learning_rate']  # KeyError if 'model' doesn't exist

# Solution: Use safe access
lr = params.get('model', {}).get('learning_rate', 0.001)
```

**Type mismatches:**
```bash
# Problem: String instead of number
--param learning_rate="0.01"  # String "0.01"

# Solution: Proper numeric syntax
--param learning_rate=0.01    # Float 0.01
```

**Complex parameter override:**
```bash
# Problem: Can't override nested list/dict from CLI
--param model.layers=[64,128]  # Doesn't work as expected

# Solution: Use JSON format with quotes
--param "model.layers=[64,128,256]"
```

---

**Related:**

- [`yanex run`](../../cli/run.md) - Running experiments with parameters
- [Python API](../../api/index.md) - Using parameters in code
- [Best Practices](../best-practices.md) - Configuration organization tips
