# Use certifi's CA bundle for HTTPS (fixes SSL errors on macOS)
import ssl
try:
    import certifi
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
except Exception:
    pass

from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root so it works regardless of current working directory
load_dotenv(Path(__file__).resolve().parent / ".env")

import sys
import time
import traceback
from fetch_feeds import fetch_all_feeds
from deduplicate import deduplicate
from score_stories import score_story
from generate_brief import rank_stories, create_brief
from send_email import send_email
from database import mark_processed
from config import RUN_INTERVAL

# Ensure logs are visible immediately (no buffering)
def log(msg):
    print(msg, flush=True)

# Only run when attached to a terminal (stops when terminal closes; won't run from cron/nohup)
if not sys.stdin.isatty():
    print("NewsAgent runs only in an interactive terminal. Close the terminal to stop it.", file=sys.stderr, flush=True)
    sys.exit(0)

log("NewsAgent starting...")
log(f"Run interval: {RUN_INTERVAL} minutes")
log("---")

def run_pipeline():
    log("Fetching feeds...")
    stories = fetch_all_feeds()

    if not stories:
        log("No new stories.")
        return

    log("Deduplicating...")
    stories = deduplicate(stories)

    n = len(stories)
    log(f"Scoring {n} stories...")
    for i, s in enumerate(stories, 1):
        log(f"  Scoring {i}/{n}: {s.get('title', '')[:50]}...")
        s["scores"] = score_story(s)
        mark_processed(s["url"])

    log("Ranking...")
    top = rank_stories(stories)

    log("Generating brief...")
    brief = create_brief(top)

    log("Sending email...")
    send_email("📰 Newsroom Brief", brief)

    log("Cycle complete.")

while True:
    try:
        run_pipeline()
    except Exception as e:
        log(f"Error: {e}")
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()

    log(f"Sleeping {RUN_INTERVAL} minutes...")
    time.sleep(RUN_INTERVAL * 60)
