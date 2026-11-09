# Your first experiment

Work inside a Git repository so Yanex can record the code revision. For a new
project, create a directory and run `git init` there.

Save the following as `experiment.py`:

```python
import yanex

rate = yanex.get_param("rate", default=0.1)
for step in range(3):
    score = 1 - rate / (step + 1)
    yanex.log_metrics({"score": score}, step=step)

yanex.save_artifact({"rate": rate, "score": score}, "summary.json")
```

Commit the script to preserve it in Git. Yanex captures changes to tracked files,
but does not capture untracked files in its Git patch.

## Run and inspect

```bash
yanex run experiment.py -p rate=0.1 -n baseline -t quickstart
yanex list -t quickstart
yanex show baseline
yanex get metric:score baseline
```

Yanex prints an experiment ID and storage path. Use the ID when names are not unique.

## Compare a sweep

```bash
yanex run experiment.py -p rate=0.1,0.2,0.3 -n 'rate-{rate}' -t quickstart
yanex compare -t quickstart --params rate --metrics score
```

Use `yanex ui` to browse experiments in the web interface, or analyze them in Python:

```python
import yanex.results as yr

df = yr.compare(tags=["quickstart"], params=["rate"], metrics=["score"])
print(df)
```

The DataFrame example requires `yanex[results]`. Python searches are global by
default; add `project="your-repository-name"` to restrict the cohort.

## Run without tracking

`python experiment.py` uses the parameter default, skips metric tracking, and
saves `summary.json` under `./artifacts/`. This makes it possible to develop a
script normally and enable tracking when needed.

Next: [core concepts](concepts.md), [configuration](../user-guide/running/configuration.md),
and [metrics and artifacts](../user-guide/running/metrics-artifacts.md).
