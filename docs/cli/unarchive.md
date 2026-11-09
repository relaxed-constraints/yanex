# `yanex unarchive` - Restore Archived Experiments

Move archived experiments back to the active experiments directory.

## Quick Start

```bash
# Unarchive specific experiments
yanex unarchive --ids a1b2c3d4,e5f67890 --global

# Unarchive all completed experiments
yanex unarchive -s completed

# Unarchive experiments with specific tag
yanex unarchive -t baseline
```

## Overview

The `yanex unarchive` command moves experiments from the archived directory back to the active experiments directory. This restores them to your main workspace where they appear in normal `yanex list` commands and are treated as active experiments.

Unarchived experiments retain all their original data including:

- Metadata (name, tags, description, status)
- Configuration parameters
- Results and metrics
- Artifacts and output files
- Environment and Git information

## Command Options

### Required Arguments

- `experiment_identifiers`: Experiment IDs or names to unarchive (optional if using filter options)

### Filter Options

- `--ids IDS`: Comma-separated experiment IDs

- `--status`, `-s STATUS`: Unarchive experiments with specific status (completed, failed, cancelled, running, staged)
- `--name`, `-n PATTERN`: Unarchive experiments matching name pattern (supports glob syntax like `*training*`)
- `--tag`, `-t TAG`: Unarchive experiments with ALL specified tags (repeatable)
- `--project`, `-p PROJECT`: Unarchive experiments from a specific project (default: auto-detected from git repo)
- `--global`, `-g`: Unarchive experiments from all projects (ignore project auto-detection)
- `--started-after DATE`: Unarchive experiments started after date/time
- `--started-before DATE`: Unarchive experiments started before date/time
- `--ended-after DATE`: Unarchive experiments ended after date/time
- `--ended-before DATE`: Unarchive experiments ended before date/time

### Control Options

- `--force`: Skip confirmation prompt
- `--format`, `-F FORMAT`: Output format (default, json, csv, markdown)
- `--help`: Show help message and exit

## Usage

### Unarchive Specific Experiments

```bash
yanex unarchive --ids a1b2c3d4,e5f67890 --global
```

Restores the specified archived experiment IDs back to the active directory.

### Unarchive by Filter Criteria

```bash
yanex unarchive -s completed -t baseline
```

Restores all archived experiments that are completed and have the "baseline" tag.

## Date Formats

The date/time options accept flexible formats:

- **Relative**: "1 week ago", "yesterday", "2 months ago"
- **Absolute**: "2024-01-01", "2024-01-15 14:30"
- **ISO format**: "2024-01-01T14:30:00"

## Output Format

Control output format with `--format` or `-F`:

```bash
# Default: human-readable progress
yanex unarchive -s completed

# JSON for scripting
yanex unarchive -s completed -F json

# CSV for reporting
yanex unarchive -s completed -F csv
```

---

**Related:**

- [`yanex archive`](archive.md) - Archive experiments
- [`yanex list`](list.md) - List experiments (use `--archived` to see archived ones)
- [`yanex show`](show.md) - View experiment details (use `--archived` for archived experiments)

## Positional-ID lookup limitation

In the current implementation, a positional ID or name can report no archived
experiments even when the directory is archived. Use the filter path to restore
specific IDs reliably:

```bash
yanex unarchive --ids abc12345 --global
```

`--global` avoids filtering the specified ID to the current project. The command
still shows the selection for confirmation unless confirmation is skipped.
