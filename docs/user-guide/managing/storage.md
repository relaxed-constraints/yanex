# Storage layout and migrations

By default, experiments live under `~/.yanex/experiments/`. Set
`YANEX_EXPERIMENTS_DIR` before launching Yanex to use another store. Python APIs
cache managers, so set this before importing and using the API.

```text
~/.yanex/experiments/
├── abc12345/
│   ├── metadata.json
│   ├── config.json
│   ├── metrics.json
│   ├── stdout.log
│   ├── stderr.log
│   └── artifacts/
│       ├── git_diff.patch
│       └── summary.json
└── archived/
    └── def67890/
```

Files are created as needed. `metadata.json` contains identity, status, timestamps,
project, Git/environment information, and dependency slots. `config.json` stores
parameters. `metrics.json` stores observations by step. Artifacts hold saved or
copied files, including a Git patch when captured. Bash-script execution can add
`script_runs.json` and separate script-output artifacts.

Use the [Results API](../../api/results/index.md) to read data instead of depending
on private storage details. Archiving moves directories under `archived/`;
deleting removes the selected run's directory.

## Storage migrations

When upgrading Yanex, preview pending migrations before applying them:

```bash
yanex migrate --all --dry-run
yanex migrate --all
```

Migrations update stored records to the current schema. They are idempotent;
already-current runs are skipped. `--all` includes active and archived runs.
Keep backups when upgrading a valuable experiment store.
See [`migrate`](../../cli/migrate.md) for targeting and output options.
