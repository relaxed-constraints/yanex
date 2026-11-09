# Python analysis and DataFrames

Install `yanex[results]` and import `yanex.results as yr`. Analysis does not require
an active experiment context. Specify `project` or IDs to keep your cohort explicit.

## Compare final results

```python
import yanex.results as yr

df = yr.compare(
    project="my-study", tags=["sweep"], status="completed",
    params=["learning_rate"], metrics=["accuracy", "loss"],
    meta=["id", "name", "status"],
)
print(df)
df.to_csv("comparison.csv", index=False)
```

Comparison columns use prefixes: `meta:id`, `param:learning_rate`, and
`metric:accuracy`. `params="auto"` and `metrics="auto"` select varying columns;
`"all"` and `"none"` provide explicit alternatives.

## Plot per-step metrics

```python
import matplotlib.pyplot as plt
import yanex.results as yr

df = yr.get_metrics(
    project="my-study", tags=["sweep"], metrics=["loss"],
    params=["learning_rate"], meta=["name"],
)
for experiment_id, rows in df.groupby("experiment_id"):
    rows = rows.sort_values("step")
    plt.plot(rows["step"], rows["value"], label=experiment_id)
plt.legend()
plt.show()
```

This is long-format data: `experiment_id`, `step`, `metric_name`, `value`, plus
requested parameter and metadata columns. Group by experiment ID to keep separate
runs separate, even when they share parameters or names.

Use `as_dataframe=False` to retrieve raw metrics without pandas.
`include_dep_params=True` includes upstream parameters for downstream comparisons.
For a whole pipeline, scope analysis through an [experiment graph](../pipelines/graphs.md).

## Work with an individual run

```python
run = yr.get_latest(project="my-study", status="completed")
if run is not None:
    print(run.get_params())
    print(run.get_metrics())
    report = run.load_artifact("summary.json")
```

See the [Results API reference](../../api/results/index.md) and
[analysis notebooks](../../examples/index.md).
