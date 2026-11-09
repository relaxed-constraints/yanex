# Python API reference

The API reference is rendered from source docstrings. Public signatures, return
values, and errors are maintained beside the implementation.

- **[Run API](run/index.md)** (`import yanex`): parameters, metrics, artifacts,
  dependencies, and experiment execution.
- **[Results API](results/index.md)** (`import yanex.results as yr`): find, inspect,
  compare, and analyze stored experiments without an active execution context.
- **[Exceptions](exceptions.md)**: errors applications may handle explicitly.
- **[Custom artifact formats](formats.md)**: register reusable serializers.

For practical workflows, see [execution patterns](../getting-started/execution-patterns.md)
and [Python analysis](../user-guide/results/python.md).
Private storage and CLI implementation modules are not part of this reference.
