#!/usr/bin/env python3
"""Create or update a Vapi assistant configuration."""

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

ASSISTANT_CONFIG = {
    "name": "Test Assistant",
    "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful voice assistant. Be concise and friendly.",
            }
        ],
    },
    "voice": {
        "provider": "11labs",
        "voiceId": "paula",
    },
    "firstMessage": "Hello! How can I help you today?",
    "analysisPlan": {
        "structuredDataPlan": {
            "enabled": True,
            "schema": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Main topic discussed"},
                    "sentiment": {
                        "type": "string",
                        "enum": ["positive", "neutral", "negative"],
                    },
                },
            },
        },
        "successEvaluationPlan": {
            "enabled": True,
            "rubric": "NumericScale",
        },
    },
}


def create_assistant():
    resp = requests.post(f"{BASE_URL}/assistant", headers=HEADERS, json=ASSISTANT_CONFIG)
    resp.raise_for_status()
    return resp.json()


def update_assistant(assistant_id: str):
    resp = requests.patch(
        f"{BASE_URL}/assistant/{assistant_id}", headers=HEADERS, json=ASSISTANT_CONFIG
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    assistant_id = sys.argv[1] if len(sys.argv) > 1 else None

    if assistant_id:
        print(f"Updating assistant: {assistant_id}")
        data = update_assistant(assistant_id)
    else:
        print("Creating new assistant...")
        data = create_assistant()

    print(json.dumps(data, indent=2))
    print(f"\nAssistant ID: {data.get('id')}")
