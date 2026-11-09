# Git tracking and reproducibility

### Automatic Tracking

Yanex automatically records:

- Current Git commit hash
- Branch name
- Working directory status (clean/dirty)
- Remote repository URL
- **Uncommitted changes patch** (automatically captured when present)

### Handling Uncommitted Changes

Yanex no longer enforces a clean git state. Instead, it automatically captures and stores any uncommitted changes as a git patch file, helping preserve the code state used by a run.

**What happens when you have uncommitted changes:**

1. Yanex detects uncommitted changes (staged or unstaged)
2. Automatically generates a patch file: `git diff HEAD`
3. **Scans the patch for potential secrets** (API keys, tokens, credentials)
4. **Validates patch size** (warns if larger than 1MB)
5. Saves the patch as `artifacts/git_diff.patch` in the experiment directory
6. Stores metadata flags: `has_uncommitted_changes` and `patch_file` location

```bash
# Works seamlessly with uncommitted changes
yanex run script.py

# Patch is automatically captured and stored
# Check experiment metadata to see if a patch was saved
yanex show <experiment_id>
```

**Patch Contents:**

- Includes both staged and unstaged changes
- Only tracks files already in the repository (excludes untracked files)
- Excludes notebook (`*.ipynb`) changes
- Can be applied to the recorded commit to restore captured tracked-file changes

**Security and Performance Checks:**

Yanex automatically scans git patches for potential security issues:

- **Secret Detection**: Uses the `detect-secrets` library to scan for API keys, tokens, credentials, and other sensitive data
- **Patch Size Validation**: Warns if patches exceed 1MB to prevent performance issues
- **Automatic Warnings**: Security findings are logged during experiment creation

```bash
# Example warning output when secrets are detected
⚠️ Potential secrets detected in git patch! Found 2 potential secret(s).
  - Base64 High Entropy String in config.py at line 42
  - Secret Keyword in credentials.txt at line 156
```

**Note**: Line numbers refer to the actual line numbers in your source files (after applying the uncommitted changes), making it easy to locate and review the flagged content.

**Security Metadata:**

The following security information is stored in experiment metadata:

- `patch_has_secrets`: Boolean indicating if potential secrets were detected
- `patch_secret_count`: Number of potential secrets found
- `patch_size_bytes`: Patch size in bytes
- `patch_size_mb`: Patch size in megabytes

```bash
# View security information
yanex show <experiment_id>
```

**Important Security Notes:**

- Secret detection may produce false positives - review findings carefully
- If secrets are detected, review your patch before sharing experiments
- Consider committing sensitive changes separately or using environment variables
- The `detect-secrets` library is automatically installed with yanex

### Best Practices

While Yanex now handles uncommitted changes gracefully, committing your code before experiments is still recommended for:

- Clean version history
- Better collaboration
- Simplified code reviews

```bash
# Recommended: Commit changes before experiments
git add .
git commit -m "Update model architecture"
yanex run train.py --tag "new-architecture"

# Also supported: Run with uncommitted changes
# Yanex automatically captures the changes as a patch
yanex run train.py --tag "experimental-changes"
```

### Cloning Experiment Configurations

Use `--clone-from` to re-run an experiment with the same configuration:

```bash
# Clone configuration from a previous experiment
yanex run train.py --clone-from abc123

# Clone and override specific parameters
yanex run train.py --clone-from abc123 --param learning_rate=0.01

# Clone configuration but use current script version
yanex run train.py --clone-from abc123
```

This is useful for:

- Re-running experiments with slight variations
- Testing bug fixes with same parameters
- Comparing different script versions with identical configs

### Reproducing Experiments with Patches

If an experiment was run with uncommitted changes, you can reproduce it by:

1. Checking out the recorded commit: `git checkout <commit_hash>`
2. Applying the saved patch: `git apply <experiment_dir>/artifacts/git_diff.patch`
3. Running the experiment again
