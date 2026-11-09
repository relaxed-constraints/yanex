# Finding and filtering experiments

Most CLI searches default to the current Git project. Combine filters to identify
a cohort, and quote glob patterns so your shell does not expand them:

```bash
yanex list -n 'train-*' -s completed -t sweep
yanex list --project my-study --started-after '1 week ago'
yanex list --global
yanex show abc12345
```

Repeated tags require all listed tags. IDs and names refer to runs; direct ID
lookups do not require changing projects. Names may be ambiguous.
Use `--project ""` to find runs with no project or `--name ""` for unnamed runs.

Python queries are global unless you pass a project explicitly:

```python
import yanex.results as yr

runs = yr.get_experiments(project="my-study", status="completed", tags=["sweep"])
for run in runs:
    print(run.id, run.name)
```

`get_experiments()` returns `Experiment` objects; `find()` returns metadata
dictionaries. `get_latest()` and `get_best()` return `None` when there is no match.
For loss minimization, use `yr.get_best("loss", maximize=False, status="completed")`.

See [shared CLI options](../../cli/filtering-output.md) and
[search API](../../api/results/search.md).
