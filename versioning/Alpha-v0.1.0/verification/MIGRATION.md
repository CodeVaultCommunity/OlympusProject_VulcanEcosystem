# Revision within the unpublished Alpha

[Português](MIGRATION.pt-br.md) · [Historical responsibility map](requirements/migration.json)

Edition remains Alpha-v0.1.0. Git baseline `78232f2` preserves the received distribution before revision. The older combined-proposal map remains historical context; it is not evidence that its original runtime was reexecuted here.

| Previous location/behavior | Current destination/decision |
| --- | --- |
| `vendor/minerva/` executable copy | Removed; explanatory `integrations/minerva/` and explicitly selected external validation. |
| Divergent `examples/task-board-ecosystem/` | `tests/fixtures/legacy-ecosystem/`, technical regression scope only. |
| Structural counterexample under examples | `tests/fixtures/structural-counterexamples/`. |
| Architecture guide mixed with general guides | `profiles/vulcan-architecture/` with EN/PT entry manuals. |
| Main business example not matching Atlas | Canonical `minimal`, `composition`, `task-board`, pinned to Atlas/Minerva inputs. |
| Reused report filenames | Unique immutable run directories; baseline reports moved to `reviews/`. |

Existing fixture databases are not automatically migrated into canonical examples. Their identifiers, validation, states and completion semantics differ. Select a new `--db` for the canonical programs. No migration engine or translator is supplied. Contract changes must be reviewed against their sources before code/data conversion.
