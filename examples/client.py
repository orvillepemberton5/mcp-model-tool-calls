"""Minimal Argolink example for gpt-6-sol; no request is made on import."""
from __future__ import annotations
import os
import requests

BASE = "https://api.argolink.io"
MODEL = "gpt-6-sol"

def request():
    key = os.environ["ARGOLINK_API_KEY"]
    body = {"model": MODEL, "input": "Return one short JSON object with key status."}
    response = requests.post(BASE + "/v1/responses", headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, json=body, timeout=60)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    print(request())
