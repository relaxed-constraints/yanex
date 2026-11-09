# Updating, archiving, and deleting

Use metadata to curate runs without repeating them:

```bash
yanex update abc12345 --set-name baseline
yanex update abc12345 --set-project my-study
yanex update abc12345 --add-tag benchmark --add-tag reviewed
```

Archiving moves a run out of active storage while keeping its data. Unarchiving
restores it. Deleting removes the selected experiment data permanently.

```bash
yanex archive abc12345
yanex unarchive --ids abc12345 --global
yanex delete abc12345
```

Review the selected IDs before confirming a bulk operation. Automatic project
selection does not remove confirmation prompts. Preserve upstream artifacts that
remaining experiments need.

For all options, see [`update`](../../cli/update.md), [`archive`](../../cli/archive.md),
[`unarchive`](../../cli/unarchive.md), and [`delete`](../../cli/delete.md).
