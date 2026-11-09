# Comparing experiments

Start with an explicit cohort and select the columns relevant to your question:

```bash
yanex compare -t sweep -s completed --params learning_rate --metrics accuracy,loss
yanex compare -t sweep -F csv > comparison.csv
```

The interactive table supports sorting and column selection. See the
[`compare` reference](../../cli/compare.md) for controls and output options.

Default automatic column selection highlights differences. For a report, select
columns explicitly so the output does not change when a parameter becomes constant.
Review failed and cancelled runs separately before limiting a scientific comparison
to successful runs.

In Python, `yr.compare()` returns a wide DataFrame with one row per experiment and
prefixed columns such as `param:learning_rate` and `metric:accuracy`. Use
`yr.get_metrics()` for per-step observations. See [Python analysis](python.md).
