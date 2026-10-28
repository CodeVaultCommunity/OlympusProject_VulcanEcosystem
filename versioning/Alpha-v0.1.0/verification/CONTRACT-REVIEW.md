# Contract preservation review

[Português](CONTRACT-REVIEW.pt-br.md) · [Integration method](../integrations/minerva/README.md)

The canonical Atlas JSON bytes are copied unchanged. Original Minerva blueprints are pinned separately; local binding revisions preserve their ADPM and scenario intent while adding observed source records and test references. Input metadata retains pending owner review. The local Minerva repository changed during this work; its clarified quality-check links and canonical invariant lists were incorporated before final verification.

Minimal preserves exact case-sensitive codes and positive integer quantities; duplicate storage does not replace data. Booking preserves uppercase code rules, independent lookup authorization, same-context composition and expected-version writes. TaskBoard preserves supplied exact identifiers/title, board-scoped context, revision zero on creation, refusal of repeated completion, conditional revision increment and consistent sorted listing.

Concrete SQLite failures distinguish confirmed refusal/not_applied from uncertain write acknowledgement; no automatic retry is introduced. Tests deliberately apply a write and lose confirmation to check that unknown does not become false success/no-change. Shared booking quality remains the source creation procedure; cancellation-specific latency is an unresolved source question. No inferred code observation or passing test constitutes stakeholder approval.

Traceable scenario outcomes, source hashes and operational limits belong to the [current receipt](RELEASE.md), not this semantic review narrative.
