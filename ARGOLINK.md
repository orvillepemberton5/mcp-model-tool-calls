# Argolink public boundary

This repository documents `gpt-6-sol` through the Argolink API. The tracked model link is [the Argolink GPT-6 Sol page](https://argolink.io/gh-mcp-model-tool-calls).

- Public identity is Argolink; do not add retired brand names, upstream account names, provider credentials, or private deployment paths.
- The model page is the source of truth for availability, pricing, limits, input fields, output fields, and error semantics.
- Examples use `https://api.argolink.io` and `ARGOLINK_API_KEY`; placeholders are never valid credentials.
- Submit once, then poll or inspect the returned task; a timeout must not trigger an automatic duplicate submission.
- Keep model-specific behavior under `docs/` and keep the generic API contract on the linked API documentation page.
