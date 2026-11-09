# Examples

Explore runnable scripts and notebooks for common Yanex workflows. Each example
includes setup instructions and explanations in its GitHub directory or notebook.

## CLI workflows

### Basic usage

Start with a small computation that reads parameters and logs metrics. Run the same script standalone or with Yanex tracking, using defaults or command-line overrides.

[Open example `01_basic_usage` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/01_basic_usage)

### Configuration files

Configure a simulated training run with nested YAML parameters. Learn how to access nested values and override individual settings from the command line.

[Open example `02_config_files` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/02_config_files)

### Saving artifacts

Save analysis outputs alongside an experiment, including text, existing files, and Matplotlib figures. The example shows how file extensions determine artifact formats.

[Open example `03_logging_artifacts` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/03_logging_artifacts)

### Names, descriptions, and tags

Organize simulated scraping runs with names, descriptions, and tags. Set metadata defaults in YAML, then use names and tags to find or clean up related experiments.

[Open example `04_metadata_and_tags` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/04_metadata_and_tags)

### Metrics across multiple steps

Track measurements over a simulated training loop using explicit or automatically incremented steps. Add metrics to an existing step and record validation measurements less frequently.

[Open example `05_multi_step_metrics` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/05_multi_step_metrics)

### Bash script integration

Run a simulated database benchmark through a Python wrapper. Pass parameters into Bash through environment variables, capture stdout and stderr as artifacts, and log execution timing from Python.

[Open example `06_bash_integration` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/06_bash_integration)

### Parameter sweeps

Explore algorithm performance across parameter combinations using lists, ranges, and linear or logarithmic spacing. Define sweeps in YAML or on the command line and execute them sequentially or in parallel.

[Open example `07_parameter_sweeps` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/07_parameter_sweeps)

### Script arguments and experiment parameters

Combine a data validation script’s argparse options with Yanex parameters. See how script-specific flags differ from configuration values tracked as experiment parameters.

[Open example `08_script_cli_arguments` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/08_script_cli_arguments)

### Staging experiments for later

Prepare system-monitoring experiments without immediately executing them. Inspect the staged runs, execute them sequentially or in parallel, and cancel runs that are no longer needed.

[Open example `09_staged_experiments` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/09_staged_experiments)

### Dependencies and multi-stage pipelines

Connect data preparation, training, and evaluation runs through named dependency slots. Reuse upstream outputs and combine dependency sweeps with parameter sweeps.

[Open example `10_dependencies` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/10_dependencies)

### Metadata templates

Generate names, tags, and descriptions from parameter values in a small batch-processing benchmark. Explore number formatting, upstream parameter lookup, conflicting dependency values, and previews before execution.

[Open example `11_metadata_templates` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/cli/11_metadata_templates)

## Python execution

### Creating experiments from Python

Use the create_experiment() context manager to track a data-processing task without the CLI. Supply configuration and metadata in Python, access experiment information, and log metrics within the managed lifecycle.

[Open example `01_creating_experiments` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/run-api/01_creating_experiments)

### Batch execution and grid search

Build a grid search with ExperimentSpec and run_multiple(). Control parallelism and inspect the returned ExperimentResult objects to identify successful and failed runs.

[Open example `02_batch_execution` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/run-api/02_batch_execution)

### K-fold cross-validation

Use one script to orchestrate a cross-validation workflow and execute individual folds. A sentinel parameter selects the mode, while the Results API retrieves completed fold metrics for aggregation.

[Open example `03_kfold_training` on GitHub](https://github.com/rueckstiess/yanex/tree/main/examples/run-api/03_kfold_training)

## Results analysis notebooks

### Reading experiment data

Retrieve experiments by ID or tag and explore their stored parameters and metrics through the Results API. The notebook includes instructions for generating the sample runs used in the analysis.

[Open example `01_reading_experiments.ipynb` on GitHub](https://github.com/rueckstiess/yanex/blob/main/examples/results-api/01_reading_experiments.ipynb)

### Filtering and comparing experiments

Turn a collection of runs into a pandas DataFrame with compare(). Filter, group, and aggregate results to investigate how parameter choices affect measured performance.

[Open example `02_filtering_comparing.ipynb` on GitHub](https://github.com/rueckstiess/yanex/blob/main/examples/results-api/02_filtering_comparing.ipynb)

### Visualizing metrics

Use get_metrics() to prepare time-series data for plotting. Compare individual runs, parameter groups, and averages, and explore measurements with different scales.

[Open example `03_metrics_visualization.ipynb` on GitHub](https://github.com/rueckstiess/yanex/blob/main/examples/results-api/03_metrics_visualization.ipynb)

### Analyzing experiment graphs

Explore a pipeline through ExperimentGraph: navigate roots and leaves, filter connected experiments, and access artifacts, parameters, and metrics across the graph. Compare runs within a pipeline and examine branching workflows.

[Open example `04_experiment_graphs.ipynb` on GitHub](https://github.com/rueckstiess/yanex/blob/main/examples/results-api/04_experiment_graphs.ipynb)
