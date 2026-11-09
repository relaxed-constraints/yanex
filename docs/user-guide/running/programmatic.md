# Programmatic execution and notebooks

## Batch execution

Create specifications in a normal Python script and pass them to `run_multiple()`:

```python
from pathlib import Path
import yanex

if __name__ == "__main__":
    specs = [
        yanex.ExperimentSpec(
            script_path=Path("train.py").resolve(),
            config={"learning_rate": lr},
            name=f"lr-{lr}",
            tags=["sweep"],
        )
        for lr in [0.001, 0.01, 0.1]
    ]
    results = yanex.run_multiple(specs, parallel=2)
    for result in results:
        print(result.experiment_id, result.status, result.error_message)
```

Run the orchestrator with `python sweep.py`. The main guard is needed for portable
multiprocessing. Child scripts use the normal `yanex.get_param()` and logging API.
Use named dependency IDs in `ExperimentSpec.dependencies` to connect pipeline stages.

The call waits for execution to finish. Individual run failures are returned as
results, so inspect every status before aggregating a batch. Sequential execution
uses `parallel=None`; `parallel=0` selects the CPU count. Processes have separate
experiment stores but share the invocation working directory and external resources.

## K-fold and ensemble workflows

Give each specification a fold index or random seed. A single script can serve as
both orchestrator and worker by checking a sentinel parameter such as `_fold_idx`.
Keep the orchestration entry point under `if __name__ == "__main__"` and ensure
child runs receive the sentinel so they do not recursively launch more batches.

See the [batch and k-fold examples](../../examples/index.md).

## Notebook experiments

Use an existing notebook path with an explicit context:

```python
from pathlib import Path
import yanex

with yanex.create_experiment(
    Path("analysis.ipynb"), name="notebook-analysis", config={"samples": 100}
) as context:
    yanex.log_metrics({"processed": yanex.get_param("samples")})
    experiment_id = context.experiment_id
```

Call logging functions on `yanex`, not on the context object. Normal context exit
marks the run completed; an unhandled exception marks it failed. A keyboard
interrupt marks it cancelled. `completed()`, `fail()`, and `cancel()` end the
context early. `create_context(id)` enters an existing experiment; it does not
restore Python variables or model checkpoints.

See [lifecycle API](../../api/run/lifecycle.md) and
[batch API](../../api/run/batch.md) for exact signatures.
