# Get started with Vulcan Ecosystem

[Português brasileiro](getting-started.pt-br.md) · [Home](../README.md) · [Selected edition](../versioning/Stable-v1.0.0/README.md)

Vulcan Stable-v1.0.0 realizes a complete Minerva Stable-v1.0.0 Markdown tree as executable code, tests, realization metadata, and a knowledge graph. Every executable or testable Minerva module maps to one code file and top-level symbol while retaining Atlas and Minerva identities.

Use Python 3.11 or later. From the repository root:

```bash
python -m pip install -e "versioning/Stable-v1.0.0"
python versioning/Stable-v1.0.0/run_examples.py
python versioning/Stable-v1.0.0/scripts/validate_ecosystem.py
python -m pytest versioning/Stable-v1.0.0/tests
```

The maintained examples contain their complete Minerva source under `docs/L2_MinervaBlueprints/` and their L3 ledgers under `docs/L3_Vulcan/`. Abstract tools become protocols, concrete-tool designs become adapters, and boundaries remain interaction adapters. Validation establishes structural and runtime evidence only within its declared scope.
