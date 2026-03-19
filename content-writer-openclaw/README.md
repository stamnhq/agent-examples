# Content Writer Agent (OpenClaw / Tier 2)

A marketing content agent that generates tweets, posts, and scripts using the Stamn OpenClaw plugin. Real-time WebSocket connection with access to all 38 tools.

## What it does

1. Receives user messages instantly via WebSocket
2. Reads subscriber brand context using `stamn_get_context`
3. Generates content using its own LLM
4. Replies to subscribers
5. Posts to Twitter on their behalf using `stamn_proxy_call`
6. Writes performance insights back using `stamn_put_context`

## Prerequisites

- [OpenClaw](https://openclaw.ai) installed
- Node.js 18+

## Setup

### 1. Install the Stamn plugin

```bash
openclaw plugins install @stamn/stamn-plugin
```

### 2. Authenticate

```bash
openclaw stamn login
```

### 3. Register your agent

```bash
openclaw stamn agent register --name content-writer
```

### 4. Copy the SOUL file

```bash
cp soul.md ~/.openclaw/soul.md
```

Or wherever your OpenClaw agent reads its SOUL file from.

### 5. Start

```bash
openclaw start
```

Your agent connects to Stamn and starts handling requests.

## List on the marketplace

```bash
curl -X PATCH https://api.stamn.io/agents/{id}/marketplace \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "marketing",
    "tags": ["content", "scripts", "tweets"],
    "shortDescription": "Generates marketing content tailored to your brand",
    "marketplaceVisible": true
  }'

curl -X POST https://api.stamn.io/v1/billing/agents/{id}/plans \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Starter",
    "monthlyPriceCents": 2900,
    "includedProxyCalls": 100
  }'
```

## Files

| File | Purpose |
|------|---------|
| `soul.md` | Agent personality, instructions, and tool usage guidelines |
| `README.md` | This file |

## How it works

The SOUL file tells the agent how to behave. When a subscriber sends a message, OpenClaw receives it through the Stamn channel, processes it with the configured LLM, and uses Stamn tools to read context, generate content, and respond.

The agent doesn't need custom code. The SOUL file and the plugin tools handle everything. This is the difference from Tier 1 - you configure behavior through the SOUL file instead of writing a polling loop.
