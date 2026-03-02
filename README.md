# News Intelligence Agent

A Python agent that fetches news from RSS feeds, scores stories for relevance using AI, and emails you a short brief with the top stories on a schedule.

---

## How it works

The agent runs in a loop. Each cycle:

1. **Fetch** — Pulls RSS feeds (BBC, NYT, Reuters, NDTV, ToI, Aaj Tak, etc.). Only stories whose URLs haven’t been seen before are kept.
2. **Deduplicate** — Removes duplicate entries by URL.
3. **Score** — Sends each story’s title and summary to OpenAI (GPT-4o-mini), which returns a relevance score from 0.0 to 1.0.
4. **Rank** — Sorts by score and keeps the top 5.
5. **Brief** — Builds a plain-text brief (title, score, link for each).
6. **Email** — Sends the brief to you via Gmail SMTP.
7. **Sleep** — Waits for the configured interval (default 30 minutes), then repeats.

Processed story URLs are stored in a local SQLite database (`news.db`) so the same story is not scored or emailed again.

---

## Prerequisites

- **Python 3.8+**
- **OpenAI API key** (for scoring)
- **Gmail** with an [App Password](https://support.google.com/accounts/answer/185833) (for sending the brief)

---

## Setup

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd "News Intelligence Agent"
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your [OpenAI API key](https://platform.openai.com/api-keys) |
| `EMAIL_USER` | Your Gmail address (e.g. `you@gmail.com`) |
| `EMAIL_PASS` | Gmail [App Password](https://support.google.com/accounts/answer/185833) (not your normal password) |
| `EMAIL_TO` | Comma-separated recipients (e.g. `you@example.com` or `a@x.com,b@y.com`) |
| `RUN_INTERVAL_MINUTES` | Optional; default `30` (minutes between cycles) |

Never commit `.env`; it is listed in `.gitignore`.

---

## How to use

Run the agent in your terminal:

```bash
python main.py
```

- The agent runs only in an **interactive terminal**. When you close the terminal, it stops. It is not intended for cron or nohup.
- Each cycle logs: fetch progress, number of stories scored, then “Cycle complete” and “Sleeping X minutes...”.
- To stop: press `Ctrl+C`.

### Example output

```
NewsAgent starting...
Run interval: 30 minutes
---
Fetching feeds...
  https://feeds.bbci.co.uk/news/rss.xml... → 50 items, 12 new
  ...
Deduplicating...
Scoring 12 stories...
  Scoring 1/12: Some headline...
  ...
Ranking...
Generating brief...
Sending email...
Cycle complete.
Sleeping 30 minutes...
```

---

## Changing feeds

Edit `config.py` and update the `FEEDS` list with any RSS/Atom feed URLs. The agent will fetch from all of them each cycle.

---

## Project layout

| File | Purpose |
|------|---------|
| `main.py` | Entry point; runs the pipeline in a loop |
| `config.py` | Loads `.env`, validates required vars, defines `FEEDS` and `RUN_INTERVAL` |
| `fetch_feeds.py` | Fetches RSS feeds, skips already-processed URLs |
| `deduplicate.py` | Deduplicates stories by URL |
| `score_stories.py` | Calls OpenAI to score each story |
| `generate_brief.py` | Ranks by score, builds top-5 brief text |
| `send_email.py` | Sends the brief via Gmail SMTP |
| `database.py` | SQLite helpers for processed URLs |
| `.env.example` | Template for `.env` (copy to `.env` and fill in) |

---

## License

Use and modify as you like. Ensure you comply with OpenAI’s and each feed’s terms of use.
