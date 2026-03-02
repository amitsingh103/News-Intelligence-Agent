from openai import OpenAI
from config import OPENAI_API_KEY

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client

def score_story(story):
    """Score a story for relevance; returns a dict with 'relevance' (0-1) and optional 'reason'."""
    try:
        client = _get_client()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Score news relevance from 0.0 to 1.0. Reply with one number only."},
                {"role": "user", "content": f"Title: {story.get('title', '')}\nSummary: {story.get('summary', '')[:500]}"},
            ],
            max_tokens=10,
            timeout=30.0,
        )
        text = (resp.choices[0].message.content or "0.5").strip()
        score = float(text) if text.replace(".", "").isdigit() else 0.5
        score = max(0.0, min(1.0, score))
        return {"relevance": score}
    except Exception:
        return {"relevance": 0.5}
