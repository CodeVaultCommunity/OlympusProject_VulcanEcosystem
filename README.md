<p align="center"><img src="assets/vulcan-banner-en.png" alt="Vulcan Ecosystem · Olympus Project · Alpha-v0.1.0" width="100%"></p>

<p align="center"><strong>Vulcan Ecosystem Alpha-v0.1.0 · OAL L3 / ADI</strong></p>

English · [Português brasileiro](README.pt-br.md)

# Vulcan Ecosystem

**Vulcan Ecosystem is an OAL L3 model for organizing and realizing applications in code.** It supplies the Vulcan Architecture profile, admits other architectures, and defines explicit composition, full or selective execution, and links to program models and verification.

Part of **Olympus Project**, alongside Atlas Specifications (L1) and Minerva Blueprints (L2).

This README is the illustrated introduction. The [edition manual](versioning/Alpha-v0.1.0/README.md) contains the textual rules. English is normative; Portuguese is its translation. The Alpha is supplied for experimentation and review; the [verification report](versioning/Alpha-v0.1.0/verification/RELEASE.md) delimits observed results.

## Contents

- [Position in Olympus](#position)
- [Ecosystem and architecture](#content)
- [Workflow](#workflow)
- [Quick start](#quick-start)
- [Documentation by layer](#documentation)
- [Examples](#examples)
- [Versions](#versions)
- [Repository organization](#repository-organization)
- [Verification and integrity](#verification)
- [Authorship and license](#authorship)

<a id="position"></a>
## Position in Olympus

<p align="center"><img src="assets/vulcan-oal-position-en.png" alt="Vulcan Ecosystem and the OAL layers" width="900"></p>

The reference is [OAL Stable-v1.0.0](https://github.com/CodeVaultCommunity/OAL_OpenAnalysisLayers). Atlas supplies L1 specifications; Minerva combines ADPM and ADVS at L2; Vulcan organizes realization at L3. Sources are pinned by revision and bytes in [source-baselines.json](versioning/Alpha-v0.1.0/verification/source-baselines.json).

<a id="content"></a>
## Ecosystem and architecture

<p align="center"><img src="assets/vulcan-model-en.png" alt="Vulcan Ecosystem: responsibilities and artifacts" width="900"></p>

An ecosystem contains identified applications under apps/. Each application declares its profile. Vulcan Architecture organizes cases, tools, entities and value objects; legacy applications retain their architecture and expose documented public operations.

Read the [identified rules](versioning/Alpha-v0.1.0/README.md#reference-rules) and [requirements mapping](versioning/Alpha-v0.1.0/verification/REQUIREMENTS.md). Model identity, profile version and a document revision remain distinct.

<a id="workflow"></a>
## Workflow

<p align="center"><img src="assets/vulcan-workflow-en.png" alt="Vulcan Ecosystem: authoring, verification and feedback" width="900"></p>

Select the program model, compose concrete tools and cases, prepare channels and run the declared modes. Record test results and compare them with specified scenarios. Libraries, abstract base classes and dependency-injection frameworks are optional.

<a id="quick-start"></a>
## Quick start

Use Python 3.11 or later. From the extracted repository root, run:

```bash
cd versioning/Alpha-v0.1.0
python -m venv .venv
# POSIX: source .venv/bin/activate
# PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run_examples.py verify
python run_examples.py list
python run_examples.py start --all --duration 10
```

The edition contains its own tools and resources. See the [manual](versioning/Alpha-v0.1.0/README.md#quick-start) for complete commands and prerequisites. The project distributes a model and reference tooling; a convenience library remains optional.

<a id="documentation"></a>
## Documentation by layer

| Recommended location | Content |
| --- | --- |
| `docs/L1_AtlasSpecifications/` | Originating cases and contracts. |
| `docs/L2_MinervaBlueprints/` | ADPM, ADVS and per-file YAML mirror. |
| `docs/L3_Vulcan/` | Organization, composition, operation, integrations and evidence. |
| `docs/Shared/` | Supporting and cross-layer material with canonical references. |

A root docs/ folder is recommended. A declared alternative may preserve the required information and links. Per-file records belong to Minerva: apps/TaskBoard/entities/Entity_Task.py maps to docs/L2_MinervaBlueprints/apps/TaskBoard/entities/Entity_Task.py.yaml. The specification repository retains its own editorial organization.

<a id="examples"></a>
## Examples

| Example | What it demonstrates |
| --- | --- |
| [TaskBoard + LegacyReports](versioning/Alpha-v0.1.0/examples/task-board-ecosystem/README.md) | Vulcan application, legacy application, HTTP, CLI, persistence and coordinated startup. |
| [Structural counterexamples](versioning/Alpha-v0.1.0/tests/) | Naming, structure and dependency violations. |

TaskBoard uses its own reconstructed didactic Atlas instance. Its contract differs from the Task Board published by Atlas. Origin, differences and limits are identified in the example documents; automatic generation and independent stakeholder approval are not claimed.

<a id="versions"></a>
## Versions

| Edition | Status | Manual and notes | Verification |
| --- | --- | --- | --- |
| Alpha-v0.1.0 | Alpha | [English](versioning/Alpha-v0.1.0/README.md#release-notes) · [Português](versioning/Alpha-v0.1.0/README.pt-br.md#release-notes) | [Report](versioning/Alpha-v0.1.0/verification/RELEASE.md) |

Each edition contains its dependencies, tools, examples and tests. This distribution contains only Alpha-v0.1.0; future revisions must preserve published snapshots and declare migrations.

<a id="repository-organization"></a>
## Repository organization

| Location | Purpose |
| --- | --- |
| `README.md`, `README.pt-br.md` | Illustrated introduction and navigation. |
| [`assets/`](assets/README.md) | Supplied icons, headers, diagrams and editable sources. |
| [`versioning/Alpha-v0.1.0/`](versioning/Alpha-v0.1.0/README.md) | Textual manual and self-contained edition. |
| [`CONTENT-SHA256.json`](CONTENT-SHA256.json) | Single byte-size and hash inventory for distribution. |
| [`scripts/`](scripts/) | Links, inventory and packaging checks. |
| [`docs/releasing.md`](docs/releasing.md) | Reproducible distribution procedure. |
| [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md) | Agent navigation and maintenance. |

<a id="verification"></a>
## Verification and integrity

```bash
python scripts/check_archive.py .
python scripts/check_repository.py
```

Run the directory audit immediately after extraction, before creating environments or caches inside it. The inventory covers every distributed file except itself, detecting missing, additional and changed files. The [release guide](docs/releasing.md) distinguishes local checks, configured CI and remote publication.

<a id="authorship"></a>
## Authorship and license

Project concept and authorship: **Douglas de Oliveira Alkimim**. This Alpha was prepared with AI assistance for review. Distributed under the [MIT license](LICENSE). Source and asset credits are in [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md); citation metadata is in [CITATION.cff](CITATION.cff).

<p><img src="https://avatars.githubusercontent.com/u/65194413?v=4" alt="Douglas de Oliveira Alkimim" width="88" height="88" align="left" hspace="12"><strong>Douglas de Oliveira Alkimim</strong><br><a href="https://github.com/douglas-alkimim">GitHub</a> · <a href="https://www.linkedin.com/in/douglas-alkimim/">LinkedIn</a></p>
<br clear="all">
