import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root (directory containing this file)
_project_root = Path(__file__).resolve().parent
load_dotenv(_project_root / ".env", override=True)

# Required env vars; missing ones will cause an immediate, loud exit
_REQUIRED = [
    "OPENAI_API_KEY",
    "EMAIL_USER",
    "EMAIL_PASS",
    "EMAIL_TO",
]

def _check_env():
    missing = [k for k in _REQUIRED if not os.getenv(k) or not str(os.getenv(k)).strip()]
    if missing:
        print("ERROR: Missing required environment variables:", file=sys.stderr, flush=True)
        for k in missing:
            print(f"  - {k}", file=sys.stderr, flush=True)
        env_path = _project_root / ".env"
        print(
            f"\nCopy .env.example to .env and add your values:\n  cp .env.example .env\n\n"
            f"Then edit {env_path} with your API key and email settings.",
            file=sys.stderr,
            flush=True,
        )
        sys.exit(1)

_check_env()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RUN_INTERVAL = int(os.getenv("RUN_INTERVAL_MINUTES", "30"))

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = [s.strip() for s in os.getenv("EMAIL_TO", "").split(",") if s.strip()]

FEEDS = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.reutersagency.com/feed/?best-topics=politics",
    "https://www.ndtv.com/rss",
    "https://timesofindia.indiatimes.com/rss.cms",
    "https://www.aajtak.in/rssfeeds",
]
