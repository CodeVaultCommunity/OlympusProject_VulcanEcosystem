# Preparing a Vulcan Ecosystem release

[Português brasileiro](releasing.pt-br.md) · [Home](../README.md) · [Agent guide](../AGENTS.md)

This procedure validates the repository distribution for the edition named by `VERSION`, currently Stable-v1.0.0. It updates that stable edition in place as authorized; it does not create another edition or authorize remote publication.

## 1. Finalize and verify

Preserve the complete Minerva source trees and their Atlas identities. Confirm every executable/testable Minerva module has one realization target, designed concrete tools are realized by adapters, Boundary remains an interaction adapter, and runtime evidence states its scope and limits.

```bash
python -m pip install -r scripts/requirements-dev.txt
python scripts/check_repository.py
python -m pytest scripts/tests
python -m pip install -e "versioning/Stable-v1.0.0"
python versioning/Stable-v1.0.0/run_examples.py
python versioning/Stable-v1.0.0/scripts/validate_ecosystem.py
python -m pytest versioning/Stable-v1.0.0/tests
```

If artwork sources changed, install `assets/requirements-artwork.txt`, regenerate with `assets/sources/render_images.py`, and inspect the derived images.

## 2. Generate the exact-byte inventory last

`CONTENT-SHA256.json` covers every present, non-ignored delivery file reported by Git except itself. It includes intentionally prepared untracked files and records relative POSIX paths, exact sizes, and SHA-256 values.

```bash
python scripts/content_inventory.py --write
python scripts/content_inventory.py --check
git status --short
```

Review all changes and ensure caches, databases, temporary outputs, and local environments remain ignored. Release history is carried by the edition and release records; no separate changelog is maintained.

## 3. Build a committed distribution only when authorized

After a separately authorized local commit leaves a clean tree:

```bash
python scripts/build_distribution.py --output /absolute/path/OlympusProject_VulcanEcosystem_Stable-v1.0.0.zip
python scripts/check_archive.py /absolute/path/OlympusProject_VulcanEcosystem_Stable-v1.0.0.zip
```

Keep the archive receipt and archive hash external. A successful local check, archive, or commit does not authorize push, tag, release, or hosted claims.
