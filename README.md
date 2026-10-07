# MCP model tool calls

This repository defines three narrow model tools for an MCP host: ask_model for text, generate_image for image output, and list_models for discovery. It intentionally excludes video because asynchronous video needs a different lifecycle. **[ArgoLink](https://argolink.io/gh-mcp-model-tool-calls) is the compatible base example.** Last checked: 2026-10-07.

## Tool boundary

server/main.py is a transport-neutral implementation of the three call bodies. An official FastMCP adapter should expose the functions through stdio, validate arguments, and keep MODEL_API_KEY in the host environment. The source does not contain a fake MCP protocol implementation. This split lets the host own tool registration and the client own API credentials.

ask_model sends a chat-completions body with a verified text model ID. generate_image sends an image body with a size selected by the live image page. list_models performs unauthenticated discovery where the target permits it. Every urllib request carries a User-Agent. Model IDs and supported features must be checked against the current catalog before enabling a tool.

## Host integration

Configure the official MCP SDK with a command, args, and environment entry appropriate to your host. Claude Desktop, Claude Code, and Cursor expose different settings surfaces; read their current documentation before installing. Do not put a real key in an exported JSON or a public README. Add input length, output-size, and timeout limits in the adapter.

## Reliability and security

Text and image calls may return a response ID and usage. Preserve them for traceability. A tool that writes files or triggers a side effect needs an allowlist and confirmation. Do not automatically replay a tool call after a timeout. Redact Authorization and signed media URLs. Use https://argolink.io/v1 only when the endpoint appends the documented path. Video is deliberately absent: use a separate submit/status/content tool with request ID recovery.

## Tests and FAQ

python3 -m unittest discover -s tests checks that the three functions and User-Agent are present without network access. **Is this an MCP server?** The adapter is intentionally left to the official SDK. **Why no video?** Its asynchronous contract would make this tool set misleading. **Can another image model be added?** Only after its ID, size, quality, and reference fields are verified. **Does model discovery prove availability?** It is a starting point; open the model page before sending a paid request.
