import re
from typing import Union
from .models import Tag

tag_regex = r'(^|[ ])#([a-zA-Z0-9]*)'


def detect_tags(entry_content: str) -> list[str]:
    matches = re.findall(tag_regex, entry_content)
    tags = []
    for match in matches:
        tags.append(match[1])
    return tags


def replace_tags_with_links(entry_content: str) -> str:

    tags = detect_tags(entry_content)

    for tag in tags:
        entry_content = entry_content.replace(f'#{tag}', f'<a href="/entries?search=%23{tag}">#{tag}</a>')

    return entry_content


def get_tag(tag_content: str) -> Union[Tag, None]:
    return Tag.query.filter(Tag.tag == tag_content).first()
