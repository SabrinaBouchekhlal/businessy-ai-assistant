
# Businessy AI Assistant — prototype

A LangChain agent with three tool-backed capabilities for a small-business dashboard:

1. **Profit Agent** — calculates revenue, listed product costs, delivery, packaging, overhead, estimated profit, and margin.
2. **Inventory Agent** — identifies items at or below their reorder threshold.
3. **Sales Agent** — summarizes order count, units sold, revenue, and revenue by product.

All three capabilities are exposed through one chat agent. The LLM selects the appropriate tool; Python computes the numbers. This avoids asking the model to do arithmetic from memory.

## Important demo limitation

The included transactions and inventory are fictional sample data. This is a read-only prototype; it is not connected to a real shop, payment provider, or live inventory database. Profit is only as complete as the recorded costs, and the demo calculation excludes taxes, returns, unpaid orders, and unrecorded expenses.

## Project structure

```text
businessy_ai_assistant/
├── backend/
│   ├── agent.py
│   ├── langgraph.json
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── branding/
│   ├── businessy-logo.svg
│   └── BRANDING.md
└── README.md
```

## 1. Set up the backend

Use Python 3.11 or 3.12.

```bash
cd backend
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your local environment file:

**Windows PowerShell**
```powershell
Copy-Item .env.example .env
```

**macOS/Linux**
```bash
cp .env.example .env
```

Open `backend/.env` and replace the placeholder with your Gemini API key. `GEMINI_MODEL` defaults to `gemini-3.8-flash`; if you need a different model, set `GEMINI_MODEL` to a model enabled for your Google AI account. Keep this file private and never commit it to GitHub.

## 2. Run the LangGraph server

Install the LangGraph CLI:

```bash
pip install -U "langgraph-cli[inmem]"
```

From the `backend` directory, run:

```bash
langgraph dev
```

The local server normally starts at `http://localhost:2024`. The graph ID is **`businessy`**.

## 3. Run the included branded UI

The bundle includes a custom responsive chat UI branded as Businessy. It is served by the same FastAPI backend, so the Gemini key remains server-side.

From the `backend` directory, after setting `.env`, run:

```bash
uvicorn api:app --reload
```

Open `http://127.0.0.1:8000`. Try the three suggested prompts in the interface.

## 4. Optional: connect the official Agent Chat UI

The official UI is maintained at https://github.com/langchain-ai/agent-chat-ui and can be created using:

```bash
npx create-agent-chat-app --project-name businessy-chat
cd businessy-chat
pnpm install
pnpm dev
```

Connect the UI to:
- Deployment URL: `http://localhost:2024`
- Assistant / graph ID: `businessy`
- LangSmith API key: not needed for local development.

See `branding/BRANDING.md` for the logo, brand palette, and recommended welcome-screen prompts.

## 5. Try these prompts

- “How much profit did I make this week?”
- “What was my revenue today?”
- “Which products need restocking?”
- “Summarize my sales this week.”
- “Which product generated the most revenue this week?”
- “Explain the difference between my revenue and estimated profit.”

The current sample data covers October 5–11, 2026. The included branded UI is a custom lightweight chat page; the backend is also compatible with the official Agent Chat UI.

## 6. Get a public link

The local URL is only accessible on your computer. To share a public link, deploy the LangGraph backend and the branded UI to hosting providers, configure the environment variables there, and connect the UI to the deployed graph URL.

A public URL cannot be created from this project folder alone; deployment requires access to your hosting accounts and configuration. Do not put your Gemini API key in a `NEXT_PUBLIC_` variable or frontend code.

For a public demo, use fictional data only. Add authentication, per-user data isolation, rate limits, and server-side secrets before allowing real users to access business records.
