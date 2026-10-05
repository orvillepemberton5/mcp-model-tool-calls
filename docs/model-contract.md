# GPT-6 Sol model contract

This table is intentionally short. Update it only after checking the live [Argolink model page](https://argolink.io/gh-mcp-model-tool-calls).

- Model ID: `gpt-6-sol`
- Argolink model page: `https://argolink.io/gh-mcp-model-tool-calls` (tracked shortlink; destination is the model page)
- Endpoint family: `/v1/responses`
- Context: `1,050,000` tokens; max output: `128000` tokens.
- Reasoning efforts: `low, medium, high, xhigh, max`; default: `medium`.
- Listed token rates: input `$2` / output `$10` per million tokens; cached input `$0.2` when listed.

## Request boundary

- Authentication: `Authorization: Bearer $ARGOLINK_API_KEY`.
- Base URL: `https://api.argolink.io`.
- Model ID: `gpt-6-sol`.
- Endpoint: `/v1/responses`.
- For media jobs, save the returned task identifier, poll the documented task endpoint, and download the final URL before its retention window ends.

Do not copy prices or limits from third-party lists into this file; the model page and catalog are the current source of truth.
