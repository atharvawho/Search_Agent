# Search_Agent 🔎🤖

A small demo project that shows a LangChain agent wired to a Google
GenerativeAI model and a search tool (TavilySearch). The repository contains
an example `main.py` which creates a React-style agent and runs a sample
query for job postings.

This README explains how to set up the project, run the example, and
notes about function-calling / tool behavior you may encounter.

## ✅ Requirements

- macOS / Linux / Windows with Python 3.13+
- A working virtual environment (recommended)
- (Optional) Google Cloud credentials or other provider API keys if you
	want live model access through the `langchain-google-genai` client.

The project `pyproject.toml` lists the libraries used; a minimal set to run
the example is listed below.

## 🚀 Quick setup

Run these commands in a zsh/bash shell from the project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
# Minimal packages used in this project - adjust versions as needed
pip install python-dotenv langchain[openai] langchain-google-genai langchain-tavily pydantic callbacks
```

If you prefer to use Poetry or another tool, you can also install from
`pyproject.toml`.

## 🔧 Configuration

Put any API keys or credentials in a `.env` file at the project root or
set environment variables. For Google GenAI you may need to set
`GOOGLE_APPLICATION_CREDENTIALS` to a service account JSON file path or
configure your environment according to the Google client library docs.

Example `.env` (only if you use environment-driven auth):

```text
# Example only — do not commit credentials to source control
# GOOGLE_API_KEY=...
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## 📁 Files of interest

| File | Purpose |
|---|---|
| `main.py` | Example entrypoint: builds the React-style agent and runs a sample query |
| `prompt.py` | Prompt template used by the agent |
| `schemas.py` | Pydantic models used for structured output |
| `README.md` | This file — usage and notes |

## ▶️ Running the example

With the virtualenv activated run:

```bash
.venv/bin/python main.py
```

The script will create an agent and invoke a sample search for job
postings. Output is printed to stdout. If you see a long streaming output
or the run appears blocked, allow it to complete (it may be streaming from
the model or the search tool) or cancel with Ctrl‑C.

## ⚠️ Common issues and troubleshooting

- ALTS/gRPC warning printed before other logs (example):
	`ALTS creds ignored. Not running on GCP and untrusted ALTS is not enabled.`
	This is informational from the gRPC library and can be ignored when not
	running on GCP.
- If the model answers from its internal knowledge ("I cannot browse") it
	likely did not call the search tool. That can happen because the model
	didn't decide to call a tool, or because provider-specific function
	calling metadata wasn't used. You can either:
	- Make the prompt explicitly ask the agent to call a named tool, or
	- Use the React agent flow (the repository's `main.py` uses this by
		default) which tends to orchestrate tool calls more reliably.
- Long-running or blocked requests: add timeouts or wrap tool calls if
	you need deterministic behavior. You can also catch KeyboardInterrupt at
	the top level to exit cleanly (the example `main.py` includes simple
	error handling).

## ✨ Next steps / Extensions

- Replace the demo `TavilySearch` usage with a real job API and add
	specific parsing for job pages.
- Implement provider-specific function-calling (if you want the model to
	automatically invoke functions/tools) — this may need additional
	configuration with your LLM provider.
- Add unit tests for parsing and result filtering.

If you'd like, I can add a short `requirements.txt`, a README section on
how to obtain API credentials, or rework `main.py` to include per-tool
timeouts and improved result filtering.

---

If anything in the repo has changed since you last ran the example (for
example, files added/removed during experiments), let me know and I can
help restore a specific previous state or clean up any leftover files.

## 📝 Example output

Below is an example of the kind of structured output you might see when
the agent returns job postings. Fields and format depend on `schemas.py`.

```json
{
	"answer": "AI Engineer (Entry Level) at ExampleAI (https://example.com/jobs/1)\nJunior ML Engineer at StartupLabs (https://example.com/jobs/2)",
	"sources": [
		{"url": "https://example.com/jobs/1"},
		{"url": "https://example.com/jobs/2"}
	]
}
```

This is a small deterministic example used for local testing. Live runs
may return different shapes depending on the tools and provider responses.

---

If anything in the repo has changed since you last ran the example (for
example, files added/removed during experiments), let me know and I can
help restore a specific previous state or clean up any leftover files.
