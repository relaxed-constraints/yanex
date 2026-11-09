# Yanex

Yanex is a lightweight, Git-aware experiment tracker for Python. Keep parameters,
metrics, artifacts, and code provenance together, then compare runs and reuse
results in multi-stage pipelines.

```python
import yanex

rate = yanex.get_param("rate", default=0.1)
yanex.log_metrics({"score": 1 - rate})
yanex.save_artifact({"rate": rate}, "settings.json")
```

Save this as `experiment.py` and run `yanex run experiment.py -p rate=0.2`.
The script also works with `python experiment.py` in standalone mode. Use
`yanex run` to enable tracking.

- **[Getting started](getting-started/installation.md)** — install Yanex and run your first experiment.
- **[User guide](user-guide/index.md)** — configuration, pipelines, analysis, and management.
- **[CLI reference](cli/index.md)** — commands and options.
- **[Python API reference](api/index.md)** — public functions and classes, rendered from source docstrings.
- **[Examples](examples/index.md)** — runnable scripts and analysis notebooks.
- **[Development](development/contributing.md)** — contribute and build the documentation.

Yanex stores experiments as local files and does not require a tracking server.
The optional web interface provides another way to browse the same data.
