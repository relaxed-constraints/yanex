# Metrics and artifacts

## Log observations by step

```python
import yanex

for epoch in range(3):
    yanex.log_metrics({"loss": 1 / (epoch + 1)}, step=epoch)
    yanex.log_metrics({"accuracy": epoch / 3}, step=epoch)
```

Calls for the same step merge their keys; logging a key again at that step
replaces its value. Omitting `step` creates the next step, starting at zero.
Use explicit steps when separate parts of your code log the same observation.
`step`, `timestamp`, and `last_updated` are reserved bookkeeping keys.
In standalone mode, metric logging does nothing.

## Save files and Python objects

```python
import yanex

yanex.save_artifact({"samples": 100}, "summary.json")
yanex.save_artifact("Finished", "status.txt")
summary = yanex.load_artifact("summary.json")
```

`copy_artifact(path)` copies an existing file. `save_artifact()` selects a serializer
from the extension: for example JSON, CSV, NumPy arrays, PyTorch models, or figures.
Install the library required for the format you use. A custom `saver` or `loader`
can handle other formats; reusable registrations use `register_format()`.
See the [artifact API](../../api/run/artifacts.md).

Standalone scripts use `./artifacts/`; tracked scripts use their experiment's
artifact directory. Avoid writing shared output files into the working directory
when running experiments in parallel.

## Reuse upstream artifacts

`load_artifact()` checks the current experiment first, then searches dependencies.
It returns `None` when the artifact is missing and raises `AmbiguousArtifactError`
when multiple dependencies provide it. Select a named dependency to resolve that:

```python
data_run = yanex.get_dependency("data")
if data_run is None:
    raise ValueError("Supply the data dependency with -D data=<id>")
data = data_run.load_artifact("dataset.json")
```

`artifact_exists()` checks only the current experiment (or local standalone
artifacts), not upstream runs. `list_artifacts(transitive=True)` includes upstream
artifacts grouped by experiment ID.
