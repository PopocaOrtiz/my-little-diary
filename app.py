from datetime import datetime
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, text
from tags import detect_tags
from tags.models import Tag, EntryTag
from typing import Union

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Entry {id}>'


@app.route('/')
def index():
    return redirect('/entries')


@app.route('/entries', methods=['POST', 'GET'])
def entries():
    if request.method == 'POST':
        entry_content = request.form['content']
        save_entry(entry_content)
        return redirect('/entries')
    else:
        search = request.args.get('search')
        paginate = get_entries(search)

        search = search if search else ''

        return render_template('entries.html', paginate=paginate, search=search)


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

    print(sql, params)

    return db.engine.execute(text(sql), params)


def save_entry(entry_content: str):
    entry = Entry(content=entry_content)
    db.session.add(entry)
    db.session.commit()

    tags = detect_tags(entry_content)
    for tag_content in tags:
        tag_exists = get_tag(tag_content)
        if not tag_exists:
            tag_exists = Tag(tag=tag_content)
            db.session.add(tag_exists)
            db.session.commit()

        entry_tag = EntryTag(tag=tag_exists.id, entry=entry.id)
        db.session.add(entry_tag)

    db.session.commit()


def get_tag(tag_content: str) -> Union[Tag, None]:
    return Tag.query.filter(Tag.tag == tag_content).first()


def main():
    search = '#one #two three'
    search = None
    entries = get_entries(search)
    entries = list(entries)
    print(f'total: {len(entries)}')
    for entry in entries:
        print(entry['content'])


if __name__ == '__main__':
    app.run(debug=True)
    # main()
