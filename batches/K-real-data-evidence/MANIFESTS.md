# Batch K manifest policy

Two manifests have intentionally different roles:

- `evidence/manifest.json` is the frozen manifest of the original uploaded
  bundle and its old internal paths. It is historical evidence and is never
  regenerated or rewritten by repository tooling.
- `artifact_manifest.json` is the deterministic, repository-wide manifest of
  every Git-tracked or untracked-nonignored file, rooted at the repository.
  This binds Batch K artifacts to their complete package, tests, registries,
  scripts, environment lock, CI, and documentation dependencies.
  `scripts/create_manifest.py --check` verifies it; an explicit `--write` is
  required to replace it after reviewed changes.

The current manifest includes the historical manifest, quarantine ledgers,
checkpoints, reports, source code, documentation, lockfile, and CI. It excludes
only itself and files already excluded by Git ignore rules. A clean-clone
`upg-preflight` fails if the current manifest is stale or a
chronology-quarantined byte changes.
