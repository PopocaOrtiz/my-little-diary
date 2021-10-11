def detect_tags(entry_content: str) -> list[str]:
    import re
    matches = re.findall(r'(^|[ ])#([a-zA-Z0-9]*)', entry_content)
    tags = []
    for match in matches:
        tags.append(match[1])
    return tags
