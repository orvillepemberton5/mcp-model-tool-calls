# Chat request boundary

`gpt-6-sol` uses `/v1/responses`. Keep the request small enough to debug and record the returned request ID.

- Authentication: `Authorization: Bearer $ARGOLINK_API_KEY`
- Model: `gpt-6-sol`
- Base URL: `https://api.argolink.io`
- Reasoning choices currently listed for this model: `low, medium, high, xhigh, max`.

Do not silently translate a timeout into a second submission. When a tool call or structured response is required, keep the response envelope and error body in the redacted diagnostic record.
