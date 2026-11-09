# Parameter, metric, and metadata keys

Canonical keys identify both the group and path:

| Group | Example |
| --- | --- |
| Parameter | `param:model.learning_rate` |
| Metric | `metric:accuracy` |
| Metadata | `meta:status` |

```bash
yanex get param:model.learning_rate abc12345
yanex get metric:accuracy abc12345
yanex get meta:status abc12345
yanex compare --params learning_rate --metrics accuracy
```

CLI key resolution accepts an unambiguous suffix such as `learning_rate`.
When multiple keys match, specify the full path. Flags such as `--params` provide
the group, and comparison selections support patterns such as `'*.learning_rate'`.

Run API `yanex.get_param()` reads the current configuration using exact dotted
paths and a fallback default. Results and graph accessors have their own lookup
contracts; consult their reference rather than assuming every accessor accepts
all CLI patterns. In particular, graph lookups report missing and ambiguous keys
instead of silently choosing a run.
