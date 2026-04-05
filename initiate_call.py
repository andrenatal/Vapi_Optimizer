#!/usr/bin/env python3
"""Initiate a Vapi call to test an assistant."""

import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.environ.get("VAPI_API_KEY")
if not VAPI_API_KEY:
    sys.exit("Error: Set the VAPI_API_KEY environment variable.")

BASE_URL = os.environ.get("VAPI_BASE_URL", "https://api.vapi.ai")
HEADERS = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}


def initiate_call(assistant_id: str, phone_number: str | None = None):
    payload = {"assistantId": assistant_id}
    if phone_number:
        payload["customer"] = {"number": phone_number}

    resp = requests.post(f"{BASE_URL}/call", headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <assistant_id> [phone_number]")

    assistant_id = sys.argv[1]
    phone_number = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Initiating call with assistant: {assistant_id}")
    data = initiate_call(assistant_id, phone_number)

    print(json.dumps(data, indent=2))
    print(f"\nCall ID: {data.get('id')}")
