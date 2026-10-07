"""MCP tools for text/image model calls; video is intentionally a separate server."""
from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from mcp.server import MCPServer

mcp = MCPServer("argolink-model-tools")
BASE_URL = os.getenv("MODEL_BASE_URL", "https://argolink.io/v1").rstrip("/")
USER_AGENT = "mcp-model-tool-calls/1.0"


def _key() -> str:
    value = os.getenv("MODEL_API_KEY", "")
    if not value:
        raise RuntimeError("MODEL_API_KEY is not configured in the MCP host environment")
    return value


def _validate_prompt(prompt: str) -> str:
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt must be a non-empty string")
    if len(prompt) > 20_000:
        raise ValueError("prompt exceeds the 20,000-character safety limit")
    return prompt.strip()


def _request_json(path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    headers = {"Authorization": "Bearer " + _key(), "User-Agent": USER_AGENT}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    request = Request(BASE_URL + path, data=data, headers=headers, method="POST" if body is not None else "GET")
    try:
        with urlopen(request, timeout=60) as response:
            parsed = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"model request failed with HTTP {error.code}") from error
    except URLError as error:
        raise RuntimeError("model request could not reach the configured endpoint") from error
    if not isinstance(parsed, dict):
        raise RuntimeError("model response must be a JSON object")
    return parsed


@mcp.tool()
def ask_model(prompt: str, model: str = "glm-5.3", reasoning_effort: str | None = None) -> dict[str, Any]:
    """Ask a verified text model one question through Chat Completions."""
    body: dict[str, Any] = {"model": model, "messages": [{"role": "user", "content": _validate_prompt(prompt)}]}
    if reasoning_effort is not None:
        if reasoning_effort not in {"none", "low", "medium", "high", "xhigh", "max"}:
            raise ValueError("unsupported reasoning_effort")
        body["reasoning_effort"] = reasoning_effort
    response = _request_json("/chat/completions", body)
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("model response did not contain choices")
    message = choices[0].get("message", {})
    return {"request_id": response.get("id"), "model": response.get("model", model), "text": message.get("content", ""), "usage": response.get("usage")}


@mcp.tool()
def generate_image(prompt: str, model: str = "gpt-image-2", size: str = "1024x1024") -> dict[str, Any]:
    """Generate one image with a model and size verified on its model page."""
    _validate_prompt(prompt)
    if size not in {"1024x1024", "1536x1024", "1024x1536", "auto"}:
        raise ValueError("unsupported image size; verify the live model page")
    response = _request_json("/images/generations", {"model": model, "prompt": prompt, "size": size})
    return {"request_id": response.get("id"), "model": response.get("model", model), "data": response.get("data"), "usage": response.get("usage")}


@mcp.tool()
def list_models() -> dict[str, Any]:
    """List models returned by the configured catalog for host-side selection."""
    response = _request_json("/models")
    data = response.get("data", [])
    if not isinstance(data, list):
        raise RuntimeError("model list response did not contain data[]")
    return {"models": [{"id": item.get("id"), "object": item.get("object"), "owned_by": item.get("owned_by")} for item in data if isinstance(item, dict)]}


def main() -> None:
    # MCP's stdio transport is the local-host default. Importing this module
    # registers tools but never starts a process or calls the API.
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
