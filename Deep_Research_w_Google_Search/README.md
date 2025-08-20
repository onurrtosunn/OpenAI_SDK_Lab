---
title: deep_research using google_search
app_file: deep_research.py
sdk: gradio
sdk_version: 5.31.0
---

## Overview
Deep-research workflow using Google Custom Search and a set of specialized agents. The app plans searches, fetches page snippets, writes a long-form markdown report, and optionally attempts to send it via email.

## Architecture
- **PlannerAgent**: Generates N search terms for the input query.
- **SearchAgent**: Calls Google Custom Search and fetches short text previews from each result.
- **WriterAgent**: Produces a detailed markdown report (>= 1000 words).
- **Email agent**: Tries to send the report as an HTML email (uses dummy addresses by default).
- **Gradio UI**: Simple UI to enter a query and stream progress + final report.

## Requirements
- Python 3.10+
- OpenAI API key (agents)
- Google Custom Search API key + CSE `cx`
- Optional: SendGrid API key (email)

Recommended packages:
- gradio, python-dotenv, pydantic, google-api-python-client, requests, beautifulsoup4, sendgrid

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U gradio python-dotenv pydantic google-api-python-client requests beautifulsoup4 sendgrid
```

## Environment Variables
Create a `.env` file in the project root:
```env
# OpenAI (required)
OPENAI_API_KEY=sk-...

# Google Custom Search (required)
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_CONTEXT=your_cse_cx_id

# SendGrid (optional)
SENDGRID_API_KEY=your_sendgrid_api_key
```
Notes:
- Set up a Google Custom Search Engine and obtain both the API key and the `cx` id.
- For SendGrid, you need a verified sender to actually send emails.

## Run
```bash
python deep_research.py
```
The Gradio UI will open in the browser. Enter a topic and click Run to stream progress and the final markdown report.

## Email (Dummy by Default)
`email_agent.py` uses dummy addresses by default:
- `your_mail_address@mail.co`

To send real emails:
1. Verify a sender in SendGrid.
2. Update `FROM_EMAIL` and `TO_EMAIL` in `email_agent.py` with real addresses.
3. Provide a valid `SENDGRID_API_KEY` in `.env`.

`send_email` returns structured results (e.g., `{ "status": "success" | "error", ... }`). The UI only shows high-level progress messages.

## Project Structure
- `deep_research.py`: Gradio app and `run` coroutine that streams results.
- `research_manager.py`: Orchestrates plan → search → report → email.
- `planner_agent.py`: Defines `PlannerAgent` and output schema.
- `search_agent.py`: Defines `SearchAgent` and wires the Google search tool.
- `google_search_agent.py`: Google Custom Search + page content preview (Requests + BeautifulSoup).
- `writer_agent.py`: Defines `WriterAgent` and report schema.
- `email_agent.py`: SendGrid HTML email (dummy addresses by default).
- `llm_as_judge.py`: Separate example (not used by the UI flow).

## Troubleshooting
- Missing `GOOGLE_SEARCH_API_KEY` / `GOOGLE_SEARCH_CONTEXT`: search output will be empty.
- Missing `SENDGRID_API_KEY`: email tool returns `status=error`; the report is still generated.
- Missing or invalid `OPENAI_API_KEY`: agent calls will fail.
- HTTP/Fetch errors: `google_search_agent.py` returns short error messages instead of content.

## Customization
- Model: update `model="gpt-4o-mini"` in agent definitions as needed.
- Number of searches: change `HOW_MANY_SEARCHES` in `planner_agent.py`.
- Content snippet length: adjust the `fetch_page_content` truncation in `google_search_agent.py`.
