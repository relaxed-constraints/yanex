# Syncing over SSH and S3

Push copies local experiments to a remote; pull copies remote experiments into
local storage. SSH uses `rsync`; S3 uses the AWS CLI. Configure access with those
tools before using Yanex.

| Target | Meaning |
| --- | --- |
| `gpu-box` | SSH host or alias, using `~/.yanex/experiments/` |
| `user@gpu-box:~/experiments` | SSH with an explicit user and path |
| `s3://my-bucket/experiments` | S3 bucket and prefix |

```bash
yanex push gpu-box --project my-study -s completed
yanex pull gpu-box --project my-study -n 'train-*'
yanex push s3://my-bucket/experiments --ids abc12345,def67890
```

Sync commands are **global by default**. They do not automatically select the
current Git project. Pass `--project` or other filters to narrow the transfer.
Pull fetches remote metadata first, applies filters, then transfers matching runs.

Both commands request confirmation; `--yes` skips it and `--progress` shows transfer
progress. When files conflict, push uses the local copy and pull uses the remote
copy. Sync is a directional transfer, not a merge of metrics or metadata.

See [`push`](../../cli/push.md) and [`pull`](../../cli/pull.md).
