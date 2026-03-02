def deduplicate(stories):
    seen = set()
    out = []
    for s in stories:
        url = s.get("url")
        if url and url not in seen:
            seen.add(url)
            out.append(s)
    return out
