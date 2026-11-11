<p align="center"><img src="assets/vulcan-banner-en.png" alt="Vulcan Ecosystem · Olympus Project" width="100%"></p>

# Vulcan Ecosystem

[Português brasileiro](README.pt-br.md) · [Stable-v1.0.0](versioning/Stable-v1.0.0/README.md) · [Verification](versioning/Stable-v1.0.0/verification/RELEASE.md)

Vulcan is the executable OAL L3 realization of Minerva. Stable-v1.0.0 consumes
the complete distributed Minerva Markdown tree and maps every `code` or `test`
target to a traceable Python file and symbol.

Each example carries its Minerva source, a `realization.json` ledger, a merged
knowledge graph, executable application code, and runtime contract tests.
Abstract tools become protocols; concrete-tool designs become verified SQLite
adapters. Public methods are checked against Minerva, not inferred from folder
names alone.

`Boundary` remains reserved for interaction adapters that expose use cases.
Behavioral scenarios and instrumentation use `observation_points`.

```powershell
cd versioning/Stable-v1.0.0
python -m pip install -e .
python run_examples.py
python scripts/validate_ecosystem.py
```

The three maintained examples contain 31 Minerva-to-code mappings and 50
passing runtime tests. The cross-layer audit proves lossless Atlas payloads,
byte-identical canonical Minerva trees, valid code symbols/methods/hashes, and
complete graph links.

The earlier [Alpha-v0.1.0](versioning/Alpha-v0.1.0/README.md) remains available
as a historical edition. Concept and authorship: Douglas de Oliveira Alkimim.
[MIT license](LICENSE) · [Contribution guide](CONTRIBUTING.md).
