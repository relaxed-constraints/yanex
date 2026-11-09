# Core concepts

An **experiment** is one execution, identified by an eight-character hexadecimal
ID. It records configuration, status, timestamps, Git information, metrics, and
artifacts. Names and tags help you find experiments; names need not be unique.

**Parameters** describe inputs and settings. **Metrics** are logged observations,
optionally indexed by step. **Artifacts** are files such as datasets, models,
figures, and reports. Keep the inputs needed to interpret a metric alongside it.

**Projects** normally use the name of the current Git repository. Most CLI
searches default to that project; direct ID lookups work across projects.
Python Results API searches and synchronization commands are global by default.

**Dependencies** connect runs through named slots such as `data` or `model`.
They allow downstream experiments to reuse artifacts and preserve pipeline
lineage. A dependency sweep creates separate runs for alternative upstream inputs.

A run normally progresses from `created` to `running`, then `completed`, `failed`,
or `cancelled`. Staging creates a `staged` experiment for later execution.
A completed run means execution succeeded; your script must check whether its
scientific or data-quality requirements were met.

See [storage](../user-guide/managing/storage.md),
[projects](../user-guide/running/metadata.md), and
[dependencies](../user-guide/pipelines/dependencies.md) for details.
