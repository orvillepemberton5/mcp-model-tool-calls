# MCP model tool calls

A focused MCP server that exposes three tools to an MCP host: `ask_model` for text, `generate_image` for image output, and `list_models` for discovery. Video is deliberately excluded because its submit/status/content lifecycle needs request-ID recovery and different approval semantics. This is an independent community server, not official MCP or ArgoLink software. **[ArgoLink](https://argolink.io/gh-mcp-model-tool-calls)** is the compatible API example. Last checked: 2026-10-07.

## Why the official SDK

The [official Python SDK](https://github.com/modelcontextprotocol/python-sdk) currently documents `MCPServer`, `@mcp.tool()`, type-hint-derived input schemas, and `mcp.run(transport="stdio")` for a local host. The server follows that shape. The SDK owns MCP framing and validation; `server/main.py` owns only the API boundary, response normalization, and safety limits. It does not print during import, so stdout remains available for stdio protocol frames.

Install and inspect the tool list:

```bash
python -m venv .venv && . .venv/bin/activate
python -m pip install -r requirements.txt
export MODEL_BASE_URL='https://argolink.io/v1'
export MODEL_API_KEY='replace-me'
python -m server.main
```

Configure an MCP host using its current JSON/settings surface. The command should point to the interpreter and `-m server.main`, with `MODEL_API_KEY` in the host's environment. Do not put a real secret in a desktop config that will be exported or committed. For a development inspector, use the SDK's documented `mcp dev` command after reviewing its version-specific behavior.

## Tool contract

### `ask_model(prompt, model="gpt-5.4", reasoning_effort=None)`

Sends `POST /v1/chat/completions` with one user message. The prompt is non-empty and capped at 20,000 characters. `reasoning_effort` is accepted only from `none`, `low`, `medium`, `high`, `xhigh`, and `max`; whether a model supports an option comes from the live catalog. The return keeps the request ID, model, text, and usage so a host can display or record them.

### `generate_image(prompt, model="gpt-image-2", size="1024x1024")`

Sends `POST /v1/images/generations`. The server accepts only documented size values (`1024x1024`, `1536x1024`, `1024x1536`, or `auto`) and returns the request ID, model, data, and usage. Verify size, quality, reference, and output URL fields against the selected image model page before adding more arguments. Signed URLs belong in a private host trace, not a public conversation.

### `list_models()`

Sends `GET /v1/models` and returns a small `{models: [...]}` list containing IDs and ownership metadata. Discovery is not feature validation: open the model page before enabling tools or billing-sensitive parameters.

Every request uses `MODEL_BASE_URL`, `MODEL_API_KEY`, a 60-second timeout, and the descriptive `User-Agent` `mcp-model-tool-calls/1.0`. HTTP errors are converted to generic messages so a key or upstream body is not leaked through MCP. The code uses no automatic retries.

## Current catalog boundary

At the 2026-10-07 check, `gpt-5.4` was a Responses model, while `glm-5.3`, `glm-5.2`, and the two DeepSeek V4 entries were Chat Completions models. The default `ask_model` value is therefore a convenience only: if the live catalog does not list Chat Completions for `gpt-5.4`, select a compatible model and use a Responses-specific tool server. Use [GET /v1/models](https://argolink.io/v1/models), [model pages](https://argolink.io/en/models), and the API [docs](https://argolink.io/en/docs) as the sources of truth.

## Host safety

- Keep the server local over stdio unless you have designed authentication for an HTTP transport.
- Add host-side confirmation for tools that write files, publish content, or spend money.
- Limit prompt, output, image size, and execution time before exposing the tool to untrusted models.
- Treat a timeout after a side-effecting request as unknown; do not replay it blindly.
- For video, use a separate tool set: submit once, poll `pending`, then download only on `done`; terminal failures are `failed` and `expired`.
- Redact Authorization, prompts, and signed media URLs from host logs.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The tests parse the source and verify tool names, transport, headers, timeout, and no-import-time request behavior. They do not install an MCP host or send a production request.
