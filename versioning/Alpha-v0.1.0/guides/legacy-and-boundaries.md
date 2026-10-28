# Legacy participation and boundary ownership

[Edition](../README.md) · [Português](legacy-and-boundaries.pt-br.md)

An app participates in a Vulcan ecosystem by publishing a faithful integration surface, lifecycle and applicable documentation. It need not refactor its interior into Vulcan Architecture. The LegacyReports example retains module-level functions and `ReportsHandler` in one `reports.py`; it makes no one-class-per-file claim.

The actual operations are `fetch_tasks`, `summarize_tasks`, `create_report`, the HTTP handler and `main`. Its L2 mirror describes those multiple units without inventing a use-case class. Its observable report contract is available; the selected TaskBoard program blueprint does not infer that every legacy internal has undergone equivalent L1-to-L2 analysis. A real unavailable interior must remain marked unavailable or unassessed.

LegacyReports calls TaskBoard's public HTTP operation with a configured read identity, verifies the primitive response shape and computes counts. It neither imports TaskBoard internals nor reads its database. The startup dependency TaskBoard → LegacyReports is a concrete L3 ordering choice; its meaning and public contract links remain recoverable from the model and interaction documentation.

For TaskBoard, `Boundary_Http` and `Boundary_Cli` adapt channel data to the same prepared use cases. The composition supplies the collaborators and trusted context resolver. L4 channel choices are documented in [interaction mappings](../examples/task-board-ecosystem/docs/Shared/interaction.md); the files being under `apps/TaskBoard/boundaries/` does not reclassify those choices as domain rules.

Public inter-app integration can also use a deliberately published library API, event or another declared mechanism. Vulcan does not require networking for every relationship. Private imports and bypassing another app's domain storage are not substitutes for a public contract. Publication must identify representations, versions, compatible behavior and failures; the receiving app cannot assume that shared field names prove equivalent semantics.

The example's baseline integration is exercised by HTTP-to-CLI consistency and a LegacyReports subprocess, as well as full startup and report-service lifecycle. It is local synchronous integration, without a distributed reliability, authentication or deployment guarantee.
