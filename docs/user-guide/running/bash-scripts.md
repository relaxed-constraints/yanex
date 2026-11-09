# Running Bash scripts

Use `yanex.execute_bash_script()` to run shell scripts and command-line tools within
a tracked experiment. This is useful for existing benchmark scripts, compiled
programs, data preparation pipelines, and tools that do not have a Python API.
A small Python wrapper connects the script to Yanex's parameters, experiment
metadata, and captured output.

## Run a script

Place these two files in the same directory. The Python wrapper runs the Bash
script and fails the experiment if the script exits with a nonzero status:

```python
# run_benchmark.py
from pathlib import Path

import yanex

yanex.execute_bash_script(
    "bash benchmark.sh",
    working_dir=Path(__file__).resolve().parent,
    raise_on_error=True,
)
```

```bash
#!/usr/bin/env bash
# benchmark.sh
set -euo pipefail

threads=${YANEX_PARAM_threads:-4}
echo "Running benchmark with $threads threads"

# Replace this with your benchmark command.
./benchmark --threads "$threads"
```

Run the wrapper using the normal CLI:

```bash
yanex run run_benchmark.py --param threads=8 --name benchmark --tag performance
```

`yanex run` currently accepts Python scripts, so run the wrapper rather than the
`.sh` file. Parameters, names, tags, and [parameter sweeps](sweeps.md) work as they
do for other experiments.

> **Current script lookup:** The helper accepts a shell command. A bare
> `"benchmark.sh"` is looked up through `PATH`; it is not automatically resolved
> beside the wrapper. The example explicitly selects Bash and sets the working
> directory so that `benchmark.sh` can be found. Despite the helper's name,
> commands otherwise use the system shell, which may not be Bash.

## Access parameters and experiment context

The script inherits the Python process's environment. During a tracked run, the
helper also supplies the experiment ID and configuration parameters:

| Variable | Contents |
| --- | --- |
| `YANEX_EXPERIMENT_ID` | Current experiment ID |
| `YANEX_PARAM_<key>` | Value of a top-level configuration parameter |
| `YANEX_EXPERIMENTS_DIR` | Experiment storage root, if configured in the parent environment |
| `YANEX_CLI_ACTIVE`, `YANEX_CLI_ARGS` | CLI context inherited when the wrapper runs through Yanex |

Parameter names retain their case: `threads` becomes `YANEX_PARAM_threads`.
Use parameter names that are valid shell variable names when accessing them with
`$VARIABLE` syntax. Dictionaries and lists are encoded as JSON; other values use
Python's string representation, including `True`, `False`, and `None`.

```bash
echo "Experiment: $YANEX_EXPERIMENT_ID"
echo "Threads: ${YANEX_PARAM_threads:-4}"
```

## Working directories and artifacts

By default, a tracked shell command runs in the **experiment directory**. The
wrapper above overrides this to run beside the scripts, which is convenient for
existing scripts that use relative paths to executables or input files.

There is currently no dedicated environment variable for the current experiment
directory or its artifacts directory. Retrieve these paths with
[`yanex get`](../../cli/get.md):

```bash
experiment_dir=$(yanex get experiment-dir "$YANEX_EXPERIMENT_ID")
artifacts_dir=$(yanex get artifacts-dir "$YANEX_EXPERIMENT_ID")

./benchmark --threads "${YANEX_PARAM_threads:-4}" \
    --output "$artifacts_dir/results.csv"
```

These lookups work regardless of the script's working directory. The `yanex`
command must be available in the script's environment. `YANEX_EXPERIMENTS_DIR`,
when set, identifies the entire store, not the current experiment directory.

Write result files into the artifacts directory to keep them with the experiment.
This also gives each run its own output location when running a parallel sweep;
files written into a shared working directory can overwrite each other.

See [Metrics and artifacts](metrics-artifacts.md) for artifact access from Python.

## Output and failure handling

Output streams to the terminal by default. Yanex also saves nonempty stdout and
stderr as `script_stdout.txt` and `script_stderr.txt` in the experiment's artifacts
directory. Set `stream_output=False` to capture output without printing it live.

Use distinct `artifact_prefix` values when executing multiple commands in one
experiment, otherwise their output artifacts use the same filenames:

```python
yanex.execute_bash_script(
    "bash prepare.sh",
    working_dir=Path(__file__).resolve().parent,
    artifact_prefix="prepare",
    raise_on_error=True,
)
```

`raise_on_error=True` raises an exception for a nonzero exit status, allowing an
unhandled script failure to fail the experiment. The default is `False`, which
returns the exit code without raising. Use `set -euo pipefail` in Bash scripts when
failed commands or pipeline stages should stop execution.

The helper returns a dictionary containing `exit_code`, `stdout`, `stderr`,
`execution_time`, `command`, and `working_directory`. Execution details are
recorded separately from metrics; they are not automatically logged as metrics.
See the [API reference](../../api/run/lifecycle.md#yanex.execute_bash_script)
for the full signature.

Without an active experiment, the helper still executes commands and returns
their results, but does not save output artifacts or inject experiment context.
Its default working directory is then the current directory. Scripts that require
an experiment ID or artifact lookup should be run through the tracked wrapper.

## Logging metrics from Bash

Yanex does not automatically interpret script output as metrics, and there is no
dedicated Bash CLI command for logging them. Choose one of these two approaches
when a script needs to report measurements.

### Return JSON to the Python wrapper

Print a JSON object to stdout, with progress messages sent to stderr:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Benchmark complete" >&2
# Replace these example values with measurements from your benchmark.
printf '{"throughput": 123.5, "latency_ms": 8.1}\n'
```

Parse the returned output and log it in the wrapper:

```python
import json
from pathlib import Path

import yanex

result = yanex.execute_bash_script(
    "bash benchmark.sh",
    working_dir=Path(__file__).resolve().parent,
    raise_on_error=True,
)
yanex.log_metrics(json.loads(result["stdout"]))
```

Keep stdout exclusively for the JSON document in this approach. This is useful
when the script reports a single set of measurements at the end of a run.

### Call Python from the Bash script

A Python process launched by the script inherits the experiment context and can
log directly into the same experiment:

```bash
python - <<'PY'
import yanex

yanex.log_metrics({"throughput": 123.5, "latency_ms": 8.1})
PY
```

Use the Python environment containing Yanex. This approach is useful for reporting
measurements during a longer script without reserving stdout for structured data.
Keep metric writes sequential rather than launching concurrent logging processes.
See [Metrics and artifacts](metrics-artifacts.md) for explicit steps and metric
updates.
