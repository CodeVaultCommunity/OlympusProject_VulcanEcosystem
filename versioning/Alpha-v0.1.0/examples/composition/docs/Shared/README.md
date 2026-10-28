# Interaction and shared assumptions

[Português](README.pt-br.md) · [Realization](../L3_Vulcan/README.md)

HTTP POST operation names and CLI JSON arguments are L4 choices. Success returns `result`; refusal/failure returns `error`; storage uncertainty additionally returns `write_outcome` (`not_applied` or `unknown`). HTTP uses 403 for denial, 400 for invalid input, 409 for domain conflict/absence, 503 for unavailable storage and 500 for invalid stored state. These status choices are projections, not new domain cases.

Only the trusted composition resolves the local token. A caller-provided actor object cannot grant access. Direct calls require a trusted context supplied by the embedding application. Default token and loopback binding are for teaching, not deployment. No browser UI is part of the canonical examples.
