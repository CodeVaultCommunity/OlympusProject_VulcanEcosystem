# Technical fixture: heterogeneous ecosystem

[Português](README.pt-br.md) · [Canonical examples](../../../examples/README.md)

Historical TaskBoard and LegacyReports support lifecycle/public-HTTP regression checks only. This is not the canonical Atlas/Minerva TaskBoard realization. The old generated identifiers, trimmed titles and idempotent completion are fixture behavior, with no ADVS equivalence claim.

`launch.py list` shows explicit registration. `launch.py start --all --duration 1` starts both default HTTP services. Selecting `--apps LegacyReports` expands its TaskBoard prerequisite. Startup verifies instance identity and cleans up owned children on failure; it never deletes persistent data or stops foreign listeners. LegacyReports retains its procedural organization and uses only public HTTP.

The edition test runner executes this fixture in a separate process to isolate its Python module names from canonical examples. All original bytes are retained in the pre-revision Git baseline; current fixture sources include Windows port ownership corrections. Source-model documentation for the discarded business example is not an active contract.
