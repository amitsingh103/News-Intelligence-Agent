import feedparser
import requests
from config import FEEDS
from database import is_processed

def fetch_all_feeds():
    stories = []

    headers = {"User-Agent": "NewsAgent/1.0 (RSS reader)"}
    for url in FEEDS:
        try:
            resp = requests.get(url, timeout=15, headers=headers)
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)
        except Exception as e:
            print(f"  {url[:50]}... → fetch error: {e}", flush=True)
            continue
        entries = getattr(feed, "entries", [])
        n_new = 0
        for entry in entries:
            link = getattr(entry, "link", "")
            if not link:
                continue
            story = {
                "title": getattr(entry, "title", ""),
                "summary": entry.get("summary", "") if "summary" in entry else "",
                "url": link,
            }
            if not is_processed(story["url"]):
                stories.append(story)
                n_new += 1
        if entries:
            print(f"  {url[:50]}... → {len(entries)} items, {n_new} new", flush=True)
        else:
            print(f"  {url[:50]}... → 0 items", flush=True)

    return stories
