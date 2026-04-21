# AutoStream Social-to-Lead Agent

Conversational AI agent for the **ServiceHive Inflx assignment**.

It supports:
- intent identification (`greeting`, `product_inquiry`, `high_intent_lead`)
- RAG-powered answers from local knowledge base
- multi-step lead qualification (`name -> email -> platform`)
- safe tool execution (`mock_lead_capture`) only after all required fields are collected
- persistent conversation state across turns using **LangGraph state**

## Tech Stack
- Python 3.9+
- LangGraph
- Streamlit
- FAISS + sentence-transformers (local retrieval)
- Gemini (`google-genai`) with fallback response logic

## Project Structure
- `app.py`: Streamlit UI and session state
- `agent/graph.py`: LangGraph workflow nodes + routing
- `agent/intent.py`: intent classification rules
- `agent/rag.py`: local knowledge loading, vector retrieval, answer generation
- `agent/tools.py`: mock lead capture tool
- `data/knowledge_base.json`: assignment KB (pricing, features, policies)

## How To Run Locally
1. Clone repository and move into project folder.
2. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional) set Gemini key for LLM responses:

```bash
export GOOGLE_API_KEY="your_key_here"
```

If no key is provided, the app still works using deterministic fallback answers.

5. Run app:

```bash
streamlit run app.py
```

## Expected Demo Flow (2-3 mins)
1. Ask: `Hi, tell me about your pricing.`
2. Agent returns plan details from RAG knowledge base.
3. Say: `I want to try the Pro plan for my YouTube channel.`
4. Agent switches to high-intent lead flow and asks for name.
5. Provide name and email.
6. Agent asks/uses platform and then triggers `mock_lead_capture`.
7. Confirm success message.

## Architecture Explanation (~200 words)
I chose **LangGraph** because the assignment requires reliable multi-turn control flow with tool-gating. A plain prompt-only bot can drift in stateful scenarios (for example, capturing email before name), but LangGraph gives explicit node transitions and deterministic branching. The workflow starts with a classification node that stores the current user message, updates conversation memory, and identifies intent. A conditional router then decides whether to answer from RAG, start lead capture, continue an in-progress lead stage, or return fallback/help text.

State is stored in a structured dictionary (`messages`, `intent`, `lead_stage`, `name`, `email`, `platform`, `lead_captured`) and persisted in Streamlit session state across turns. This satisfies the memory requirement for 5-6+ turns and keeps the assistant consistent even when the user switches between product questions and signup steps. RAG is implemented using a local knowledge base JSON, sentence-transformer embeddings, and a FAISS index. Retrieval fetches top relevant chunks and answer generation uses Gemini when available, with a deterministic fallback path for reliability. Tool execution is isolated in `mock_lead_capture`, and the graph only reaches that call after all required entities are present, preventing premature lead capture.

## WhatsApp Deployment (Webhook Design)
To integrate with WhatsApp, I would expose this agent behind a webhook API (FastAPI/Flask) and connect it to either:
- **Meta WhatsApp Cloud API**, or
- **Twilio WhatsApp Sandbox/API**.

Flow:
1. WhatsApp sends inbound message event to webhook.
2. Webhook maps sender phone number to a conversation state store (Redis/Postgres).
3. Backend calls `process_message(state, text)` from this project.
4. Response is sent back via WhatsApp send-message API.
5. Updated state is persisted for next turn.

Production additions:
- verify webhook signatures
- rate limiting and retry handling
- PII-safe logging and encrypted storage for email/name
- background queue for CRM sync after lead capture
- observability (trace each turn, tool call, and failure path)

## Notes
- Knowledge base file required by assignment is at `data/knowledge_base.json`.
- Lead tool also prints this exact assignment-style line on execution:
  `Lead captured successfully: <name>, <email>, <platform>`
