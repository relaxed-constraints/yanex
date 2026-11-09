# Names, tags, projects, and metadata templates

## Organising runs

Use names for readable labels and tags for cohorts. Names can repeat; prefer IDs
when referring to a specific run. A project defaults to the Git repository name.

```bash
yanex run train.py -n baseline -t training --project my-study
yanex list --project my-study
yanex list --global
yanex update --set-project my-study abc12345
```

Set `yanex.project` in YAML to override automatic project detection. Outside a
Git repository, CLI searches default to global scope. `--project ""` selects
experiments with no project. Direct ID lookups are always global.

## Parameter templates

Names, tags, and descriptions support placeholders resolved from each experiment's
parameters, including YAML defaults under `yanex.name`, `yanex.tag`, and
`yanex.description`:

```bash
yanex run benchmark.py -p batch_size=10,50,100,200 \
  -n "benchmark-mongodb-bs-{batch_size}" \
  -t "batch-{batch_size}" \
  -d "Benchmark using batch size {batch_size}"
```

Nested parameter paths such as `{model.learning_rate}` and unambiguous suffixes
such as `{learning_rate}` work. Python format specifications are supported:
`{learning_rate:.2f}` displays two decimal places, `{learning_rate:.3g}` displays
three significant digits, and `{seed:03d}` pads an integer with zeros. Formatting
does not change stored parameter values.

Lookup checks the current experiment's parameters first. If a key is absent
locally, it searches the selected dependencies and all their upstream ancestors,
including archived experiments. Downstream experiments and sibling branches are
excluded, and a shared ancestor is counted once. Malformed dependency metadata
causes an error instead of silently truncating the search. Upstream configurations
and dependency links are cached within each invocation and shared across sweep
combinations; separate commands read fresh data.

Repeated occurrences of the same parameter path are accepted when their values
agree, using the same behavior as `ExperimentGraph.get_param()`. Conflicting
values fail with the source experiment IDs and values. Different matching paths
(such as `model.lr` and `optimizer.lr`) remain ambiguous even when their values
agree; use a more specific path. Local ambiguity fails immediately rather than
falling back upstream. A local parameter override takes precedence over upstream
values, including conflicting upstream values.

For example, if a selected training experiment or its ancestor records
`model.learning_rate`, it can be used in an evaluation name:

```bash
yanex run evaluate.py -D model=abc12345 \
  -n "evaluation-lr-{learning_rate:.3g}" \
  -d "Evaluation of learning rate {model.learning_rate}"
```

Each dependency-sweep combination uses its own selected ancestors. Dependency
IDs and statuses, missing or ambiguous keys, malformed templates, invalid format
specifications, and invalid rendered metadata are checked before any member of
the sweep is created or executed. `--dry-run` previews rendered metadata for each
combination. Staging stores the rendered strings; executing a staged run does not
render them again.

A name containing any placeholder replaces automatic sweep naming completely.
Without placeholders, existing sweep suffixes are retained. Templates in tags or
descriptions alone do not change naming. Duplicate names remain permitted.

Use `{{` and `}}` for literal braces in template input. Substituted values are
never interpreted as templates again. Expressions, attribute access, indexing,
conversion flags (`!r`), and nested format specifications are not supported;
dots always refer to parameter paths, not Python object attributes.

Names allow printable Unicode characters, spaces, and punctuation except glob
characters (`*`, `?`, `[` and `]`). Tags allow printable Unicode characters except
whitespace, commas, and those glob characters, with a maximum of 50 characters. Descriptions
allow printable characters plus newlines and tabs, with a maximum of 1,000
characters. Validation applies after substitution. Shell-sensitive punctuation
must be quoted appropriately when passed on the command line.
