
# Businessy backend

This is the LangGraph backend used by the Agent Chat UI.

## Local setup

1. Install Python 3.11 or 3.12.
2. Create and activate a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env`, set `GOOGLE_API_KEY`, and use a Gemini model available to your account (the default is `gemini-3.8-flash`).
5. Install CLI: `pip install -U "langgraph-cli[inmem]"`.
6. Run `langgraph dev` from this directory.
7. Connect Agent Chat UI to `http://localhost:2024`, graph ID `businessy`.

## Tools

- `calculate_profit(period)`: calculates the estimate using Python arithmetic.
- `check_stock()`: reports inventory and products at/below reorder level.
- `get_sales(period)`: returns sales totals and product breakdown.

The data is hard-coded fictional demo data in `agent.py`; replace it with authenticated database queries before real use.

## Run the included branded web UI

After installing requirements and setting `GOOGLE_API_KEY` in `.env`, run:

```bash
uvicorn api:app --reload
```

Open `http://127.0.0.1:8000`. This serves the branded frontend and `/api/chat` endpoint from the same local server. The Gemini key is read server-side and is never sent to the browser.
