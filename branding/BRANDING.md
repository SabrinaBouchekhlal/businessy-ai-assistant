
# Businessy branding for Agent Chat UI

The backend graph is named `businessy`. It is compatible with the official LangChain Agent Chat UI:
https://github.com/langchain-ai/agent-chat-ui

## Recommended UI setup

1. Install Node.js LTS and pnpm.
2. Create a UI project:
   ```bash
   npx create-agent-chat-app --project-name businessy-chat
   cd businessy-chat
   pnpm install
   ```
3. Start the backend following `backend/README.md`, then configure the UI:
   - Development deployment URL: `http://localhost:2024`
   - Assistant / graph ID: `businessy`
   - No LangSmith API key is needed for local development.
4. Apply the brand:
   - Use `businessy-logo.svg` as the logo asset.
   - Change the browser title to `Businessy AI Assistant`.
   - Change the header brand text to `Businessy`.
   - Use the brand palette below in the UI's global stylesheet/theme.
   - Add the sample prompt chips from the README.
5. Run the UI with `pnpm dev`.

## Brand palette

- Forest green: `#123B32`
- Lime accent: `#D8F36A`
- Warm background: `#F7F3E8`
- Ink: `#18231F`
- Muted text: `#6E7973`
- White: `#FFFFFF`

## Suggested welcome screen

**Businessy AI Assistant**
Your small-business co-pilot.

Suggested prompts:
- “How much profit did I make this week?”
- “Which products need restocking?”
- “Summarize my sales this week.”

Use the logo in `businessy-logo.svg`. The app should clearly indicate that this prototype uses sample data.
