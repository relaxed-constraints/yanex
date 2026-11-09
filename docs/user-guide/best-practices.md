# Best practices and troubleshooting

## Organizing experiments

Use projects for repositories or studies, tags for cohorts, and names for readable
labels. Record important IDs in your research notes. Prefer metadata templates for
sweeps so labels describe the parameters actually used.
See [names, tags, and projects](running/metadata.md).

## Configuration strategies

Keep shared defaults in a base YAML file and study-specific overrides in another.
Pass files explicitly for reproducible runs. Use code defaults for standalone
development and record the full configuration for tracked comparisons.
See [configuration](running/configuration.md).

## When to use what

Start with CLI-driven scripts. Use explicit contexts for notebooks and
`run_multiple()` for Python orchestration. Keep downstream analysis in the Results
API. See [execution patterns](../getting-started/execution-patterns.md).

## Metric logging strategies

Use explicit steps when multiple calls describe the same observation. Repeated
keys at one step overwrite earlier values. Keep separate observations on separate
steps and avoid multiple concurrent writers to the same experiment.
See [metrics and artifacts](running/metrics-artifacts.md).

## Parameter sweep strategies

Preview a sweep with `--dry-run`, then test a small cohort before scaling up.
Multiple parameter and dependency sweeps form a Cartesian product. Choose
parallelism based on memory, GPUs, databases, and other shared resources as well
as CPU count. See [sweeps](running/sweeps.md).

## Git workflow integration

Commit reusable scripts and configurations. Yanex captures tracked changes, but a
patch does not preserve untracked files, notebook changes, input datasets, or
external service state. Record or save those inputs separately. `--clone-from`
reuses configuration; it does not check out the original code automatically.
See [Git tracking and reproducibility](managing/reproducibility.md).

## Debugging failed experiments

```bash
yanex list -s failed
yanex show abc12345
yanex get stderr abc12345
yanex open abc12345
```

Inspect the recorded parameters and process logs. After fixing the problem, create
a new run with `yanex run script.py --clone-from abc12345`. Preserve the original
failure when it helps explain a study. Check batch result statuses before combining
metrics; a completed process alone does not establish scientific correctness.

## Performance tips

Filter cohorts before loading artifacts or constructing DataFrames. Select explicit
columns for exported reports. Reuse completed upstream experiments through named
dependencies instead of recomputing shared preparation work. Archive old cohorts
when they are no longer part of active analysis.

## Missing runs or artifacts

Check the project filter and `YANEX_EXPERIMENTS_DIR` first. CLI searches may be
project-scoped while Python queries are global. For ambiguous artifacts, select a
named dependency explicitly. Do not assume that `artifact_exists()` searches
upstream just because `load_artifact()` does.
