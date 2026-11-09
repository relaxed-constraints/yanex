# Web interface (beta)

> **Beta — work in progress.** The web interface is under active development.
> Features and workflows may change, and some functionality is still incomplete.

Launch the browser interface over your local experiment store:

```bash
yanex ui
```

Open the URL printed by the command. Use the interface to browse runs, inspect
parameters and metrics, and compare experiments. The CLI and Python API read the
same stored experiments.

Use `yanex ui --port 8080` if the default port is occupied. See
[`yanex ui`](../../cli/ui.md) for host settings and troubleshooting.
