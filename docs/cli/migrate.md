# yanex migrate

Apply pending storage-schema migrations.

```bash
yanex migrate --all --dry-run
yanex migrate --all
yanex migrate abc12345 def67890
yanex migrate -s completed --ended-before '1 month ago'
```

Provide experiment identifiers, selection filters, or `--all`. `--all` includes
active and archived experiments and cannot be combined with identifiers or
selection filters. Current records are skipped.

| Option | Purpose |
| --- | --- |
| `--dry-run` | Preview without changing records |
| `--force` | Skip confirmation |
| `--all` | Include active and archived experiments |
| `-F json`, `-F csv`, `-F markdown` | Structured result output |

See [storage and migrations](../user-guide/managing/storage.md).
