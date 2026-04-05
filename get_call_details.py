#!/usr/bin/env python3
"""Retrieve call details, transcript, and recording from Vapi."""

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
}


def get_call_details(call_id: str):
    resp = requests.get(f"{BASE_URL}/call/{call_id}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def print_section(title: str, content: str):
    print(f"\n{'=' * 40}")
    print(f"  {title}")
    print(f"{'=' * 40}")
    print(content)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <call_id>")

    call_id = sys.argv[1]
    print(f"Fetching details for call: {call_id}")

    data = get_call_details(call_id)

    # Call summary
    summary = {
        "id": data.get("id"),
        "status": data.get("status"),
        "type": data.get("type"),
        "startedAt": data.get("startedAt"),
        "endedAt": data.get("endedAt"),
        "cost": data.get("cost"),
        "assistantId": data.get("assistantId"),
    }
    print_section("Call Details", json.dumps(summary, indent=2))

    # Transcript
    artifact = data.get("artifact", {})
    transcript = artifact.get("transcript")
    print_section("Transcript", transcript if transcript else "(no transcript available)")

    # Recording
    recording_url = artifact.get("recordingUrl") or artifact.get("recording")
    print_section(
        "Recording",
        f"URL: {recording_url}" if recording_url else "(no recording available)",
    )

    # Messages
    messages = artifact.get("messages")
    if messages:
        lines = []
        for msg in messages:
            role = msg.get("role", "unknown")
            time = msg.get("time", "")
            content = msg.get("content") or msg.get("message") or "(non-text)"
            lines.append(f"{role} [{time}]> {content}")
        print_section("Messages", "\n".join(lines))
    else:
        print_section("Messages", "(no messages available)")

    # Analysis
    analysis = data.get("analysis")
    if analysis:
        print_section("Analysis", json.dumps(analysis, indent=2))
    else:
        print_section("Analysis", "(no analysis available)")
