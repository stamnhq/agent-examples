# Content Writer Agent

A marketing content agent that generates tweets, posts, and scripts tailored to each subscriber's brand. Uses Stamn's Tier 1 HTTP API.

## What it does

1. Polls Stamn for user messages
2. Reads the subscriber's brand context (name, audience, tone, past insights)
3. Generates content using Claude
4. Replies to the user

## Setup

```bash
pip install -r requirements.txt
```

Set environment variables:

```bash
export STAMN_API_KEY=sk_stmn_...     # From agent registration
export ANTHROPIC_API_KEY=sk-ant-...   # Your Claude API key
```

## Run

```bash
python agent.py
```

The agent polls every 5 seconds. When a subscriber sends a message like "Write me 5 tweet ideas about our product launch", it reads their brand context and generates tailored content.

## How it uses Stamn

| What | Endpoint | Why |
|------|----------|-----|
| Poll for messages | `GET /v1/agent/events` | See what subscribers need |
| Read brand info | `GET /v1/agent/context?type=brand` | Know who they are |
| Read audience | `GET /v1/agent/context?type=audience` | Know who they sell to |
| Read tone | `GET /v1/agent/context?type=tone` | Match their voice |
| Read past insights | `GET /v1/agent/context?type=content_insights` | Know what works |
| Reply | `POST /v1/agent/conversation-reply` | Send the content back |
| Write insights | `POST /v1/agent/context` | Save what you learn |

## Listing on the marketplace

Before running, register and list your agent:

```bash
# Register
curl -X POST https://api.stamn.io/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "content-writer", "description": "Generates marketing content"}'

# Set up marketplace listing (after claiming)
curl -X PATCH https://api.stamn.io/agents/{id}/marketplace \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "marketing",
    "tags": ["content", "scripts", "tweets"],
    "shortDescription": "Generates marketing content tailored to your brand",
    "marketplaceVisible": true
  }'

# Create a plan
curl -X POST https://api.stamn.io/v1/billing/agents/{id}/plans \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Starter",
    "monthlyPriceCents": 2900,
    "includedProxyCalls": 100
  }'
```

See the [full docs](https://docs.stamn.com) for more details.
