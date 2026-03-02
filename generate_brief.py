def rank_stories(stories, top_n=5):
    """Return top stories by relevance score."""
    scored = [s for s in stories if s.get("scores") and "relevance" in s["scores"]]
    scored.sort(key=lambda s: s["scores"]["relevance"], reverse=True)
    return scored[:top_n]

def create_brief(top_stories):
    """Format top stories into a plain-text brief."""
    lines = ["📰 Newsroom Brief", "", "Top stories:", ""]
    for i, s in enumerate(top_stories, 1):
        title = s.get("title", "No title")
        url = s.get("url", "")
        score = s.get("scores", {}).get("relevance", 0)
        lines.append(f"{i}. {title}")
        lines.append(f"   Score: {score:.2f} | {url}")
        lines.append("")
    return "\n".join(lines)
