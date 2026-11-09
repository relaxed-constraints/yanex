# Architecture

Yanex has three user interfaces over shared experiment storage:

- **CLI:** Click commands under `yanex/cli/`, with shared filtering, formatting,
  validation, and error handling.
- **Run API:** `yanex/api.py` supplies the execution context and logging functions;
  `yanex/executor.py` runs batches in subprocesses.
- **Results API:** `yanex/results/` provides experiment objects, queries, DataFrames,
  and pipeline graphs.

`ExperimentManager` coordinates lifecycle, configuration, Git provenance, and
storage. Storage uses composable components under `yanex/core/storage_*.py`.
Dependency traversal and canonical key resolution are shared core services.

The web interface combines a FastAPI backend with a Next.js static frontend in
`yanex/web/`. Sync transports under `yanex/sync/` use SSH/rsync or the AWS CLI.

Keep user-facing examples on public APIs; internal module layouts can change.
