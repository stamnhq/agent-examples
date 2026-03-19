"""
Content Writer Agent for Stamn (Tier 1 HTTP API)

A marketing content agent that generates tweets, posts, and scripts
tailored to each subscriber's brand. Uses the Stamn API to read
brand context, respond to user messages, and write insights back.

Setup:
  1. Register your agent at https://stamn.com
  2. Set STAMN_API_KEY and ANTHROPIC_API_KEY environment variables
  3. pip install -r requirements.txt
  4. python agent.py
"""

import os
import time
import json
import requests
from anthropic import Anthropic

STAMN_API = os.environ.get("STAMN_API_URL", "https://api.stamn.io") + "/v1/agent"
STAMN_KEY = os.environ["STAMN_API_KEY"]
HEADERS = {"X-API-Key": STAMN_KEY, "Content-Type": "application/json"}

anthropic = Anthropic()


def get_events():
    res = requests.get(f"{STAMN_API}/events", headers=HEADERS)
    res.raise_for_status()
    return res.json().get("data", {})


def get_context(user_id, context_type):
    res = requests.get(
        f"{STAMN_API}/context",
        headers=HEADERS,
        params={"userId": user_id, "type": context_type},
    )
    if not res.ok:
        return {}
    entries = res.json().get("data", {}).get("entries", [])
    return entries[0]["data"] if entries else {}


def reply(user_id, text):
    requests.post(
        f"{STAMN_API}/conversation-reply",
        headers=HEADERS,
        json={"userId": user_id, "text": text},
    )


def write_context(user_id, context_type, key, data, method=""):
    requests.post(
        f"{STAMN_API}/context",
        headers=HEADERS,
        json={
            "userId": user_id,
            "type": context_type,
            "key": key,
            "data": data,
            "confidence": "derived",
            "source": {"method": method},
        },
    )


def build_system_prompt(user_id):
    brand = get_context(user_id, "brand")
    audience = get_context(user_id, "audience")
    tone = get_context(user_id, "tone")
    insights = get_context(user_id, "content_insights")

    parts = ["You are a marketing content writer."]

    if brand:
        parts.append(f"Brand: {brand.get('name', 'Unknown')}")
        if brand.get("mission"):
            parts.append(f"Mission: {brand['mission']}")
        if brand.get("industry"):
            parts.append(f"Industry: {brand['industry']}")

    if audience:
        if audience.get("demographics"):
            parts.append(f"Audience: {audience['demographics']}")
        if audience.get("painPoints"):
            parts.append(f"Pain points: {', '.join(audience['painPoints'])}")

    if tone:
        if tone.get("voice"):
            parts.append(f"Voice: {tone['voice']}")
        if tone.get("formality"):
            parts.append(f"Formality: {tone['formality']}")
        if tone.get("doExamples"):
            parts.append(f"Good examples: {', '.join(tone['doExamples'])}")
        if tone.get("dontExamples"):
            parts.append(f"Avoid: {', '.join(tone['dontExamples'])}")

    if insights:
        if insights.get("topTopics"):
            parts.append(f"Top performing topics: {', '.join(insights['topTopics'])}")
        if insights.get("bestFormats"):
            parts.append(f"Best formats: {', '.join(insights['bestFormats'])}")

    return "\n".join(parts)


def generate(user_id, message):
    system = build_system_prompt(user_id)

    response = anthropic.messages.create(
        model="claude-sonnet-4-5-20250514",
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": message}],
    )

    return response.content[0].text


def main():
    print("Content Writer Agent running. Polling for events...")

    while True:
        try:
            events = get_events()
            conversations = events.get("pendingConversations", [])

            for conv in conversations:
                user_id = conv["userId"]
                message = conv["latestMessage"]
                print(f"Message from {user_id}: {message[:80]}")

                response = generate(user_id, message)
                reply(user_id, response)
                print(f"Replied to {user_id}")

        except KeyboardInterrupt:
            print("Shutting down.")
            break
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(5)


if __name__ == "__main__":
    main()
