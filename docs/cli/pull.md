# yanex pull

Transfer experiments from an SSH or S3 target.

```text
yanex pull TARGET [FILTERS] [--yes] [--progress]
```

```bash
yanex pull gpu-box --project my-study -s completed
yanex pull user@gpu-box:~/experiments -n 'train-*'
yanex pull s3://my-bucket/experiments --ids abc12345,def67890
```

`TARGET` accepts an SSH host, `host:path`, `user@host:path`, or an S3 URL.
The default SSH directory is `~/.yanex/experiments/`.

- Filters include IDs, name, status, tags, script, project, and time bounds.
- Global project scope is the default.
- `--yes` / `-y` skips confirmation.
- `--progress` displays transfer progress.

Remote files overwrite conflicting local files. Remote metadata is read before filtering.

See [sync setup and semantics](../user-guide/managing/sync.md).
Run `yanex pull --help` for the complete option list.
