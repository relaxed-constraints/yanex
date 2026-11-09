# yanex push

Transfer experiments to an SSH or S3 target.

```text
yanex push TARGET [FILTERS] [--yes] [--progress]
```

```bash
yanex push gpu-box --project my-study -s completed
yanex push user@gpu-box:~/experiments -n 'train-*'
yanex push s3://my-bucket/experiments --ids abc12345,def67890
```

`TARGET` accepts an SSH host, `host:path`, `user@host:path`, or an S3 URL.
The default SSH directory is `~/.yanex/experiments/`.

- Filters include IDs, name, status, tags, script, project, and time bounds.
- Global project scope is the default.
- `--yes` / `-y` skips confirmation.
- `--progress` displays transfer progress.

Local files overwrite conflicting remote files.

See [sync setup and semantics](../user-guide/managing/sync.md).
Run `yanex push --help` for the complete option list.
