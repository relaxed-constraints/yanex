# Choosing an execution pattern

## CLI-driven scripts

This is the usual starting point. Call `yanex.get_param()`, `yanex.log_metrics()`,
and artifact functions directly in your script, then run it with `yanex run`.
Yanex establishes the experiment context. The same script can run standalone.

```python
import yanex

samples = yanex.get_param("samples", default=100)
yanex.log_metrics({"processed": samples})
```

```bash
yanex run experiment.py -p samples=200
```

## Explicit Python contexts

For notebooks or programmatic control, create an experiment with a context manager.
Use an existing script or notebook path and call the module-level logging functions:

```python
from pathlib import Path
import yanex

with yanex.create_experiment(Path("analysis.ipynb"), name="analysis", config={"samples": 200}):
    yanex.log_metrics({"processed": yanex.get_param("samples")})
```

Run this code directly, not through `yanex run`: creating an explicit experiment
inside a CLI-managed script raises `ExperimentContextError`. A notebook's changes
are not included in the captured Git patch, so commit the notebook separately.

## Batch orchestration

Use `ExperimentSpec` and `run_multiple()` to launch scripts from Python.
See [programmatic execution](../user-guide/running/programmatic.md) for grid search
and notebook workflows. Use the [Results API](../api/results/index.md) for analysis
after execution; it does not require an active experiment context.
