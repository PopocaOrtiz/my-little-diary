from typing import Union

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from tags import detect_tags, replace_tags_with_links

db = SQLAlchemy()


def get_entries(search: Union[str, None], page=0) -> list[dict]:
    sql = """
        select content, date_created
        from entry  
        where true
    """

    params = {}

    if search:

        tags = detect_tags(search)
        if len(tags):

            for i, tag in enumerate(tags):
                sql_tags = f"""
                    select entry
                    from entry_tag
                    join tag on entry_tag.tag = tag.id
                    where tag.tag like :tag_{i}
                """
                params[f'tag_{i}'] = tag
                sql += f"""
                    and id in (
                        {sql_tags} 
                    )
                """

                # clear the search text so it no longer has the tags
                search = search.replace(f'#{tag}', '')

        search = search.strip()
        if search:
            sql += f"""
                and content like :content 
            """
            params['content'] = f'%{search}'

    sql += f"""
        order by date_created desc
        limit 10 offset {page * 10}
    """

    entries = db.engine.execute(text(sql), params)

    entries_parsed = []
    for entry in entries:
        entry_to_parse = dict(entry)
        entry_to_parse['content'] = replace_tags_with_links(entry['content'])
        entries_parsed.append(entry_to_parse)

    return entries_parsed
