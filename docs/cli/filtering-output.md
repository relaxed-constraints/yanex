# Shared filtering and output options

Most search and management commands support a common filter vocabulary. See each
command's page or `yanex COMMAND --help` for the options available on that command.

| Option | Selects |
| --- | --- |
| `--ids a1b2c3d4,e5f67890` | Explicit experiment IDs |
| `--name 'train-*'` / `-n` | Names matching a glob pattern |
| `--status completed` / `-s` | Status |
| `--tag sweep` / `-t` | Tag; repeat to require all tags |
| `--script 'train.py'` | Script pattern |
| `--project my-study` / `-p` | Project |
| `--global` / `-g` | All projects |
| `--started-after`, `--started-before` | Start-time bounds |
| `--ended-after`, `--ended-before` | End-time bounds |

Dates accept ISO dates and natural-language values such as `'1 week ago'`.
Quote patterns and values containing spaces.

Most CLI searches automatically select the current Git project. Direct ID lookups
work globally. `push` and `pull` default to global scope. Python API searches also
require an explicit `project` filter when you want project scoping.

`yanex run -p` means `--param`, not `--project`; use the long `--project` option there.

## Output

Commands supporting structured output accept `-F json`, `-F csv`, or `-F markdown`.
`get` also provides sweep output for shell substitution. Sync commands have their
own progress output and do not provide this format option.

```bash
yanex list -t sweep -F json
yanex compare -t sweep -F csv > comparison.csv
yanex get param:learning_rate abc12345
```

See [automation](../user-guide/automation.md) for shell and agent workflows.
