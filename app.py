from datetime import datetime
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from tags import detect_tags
from tags.models import Tag, EntryTag

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


@app.route('/entries', methods=['POST','GET'])
def entries():
    if request.method == 'POST':
        entry_content = request.form['content']
        save_entry(entry_content)
        return redirect('/entries')
    else:
        search = request.args.get('search')
        query = Entry.query
        if search:
            query = query.filter(Entry.content.like(f'%{search}'))
        else:
            search = ''

        query = query.order_by(desc(Entry.date_created))

        per_page = 10
        page = request.args.get('page')
        page = int(page) if page else 1
        paginate = query.paginate(page, per_page, error_out=False)

        # return str(query)

        return render_template('entries.html', paginate=paginate, search=search)


def save_entry(entry_content: str):

    entry = Entry(content=entry_content)
    db.session.add(entry)
    db.session.commit()

    tags = detect_tags(entry_content)
    for tag_content in tags:
        tag_exists = Tag.query.filter(Tag.tag==tag_content).first()
        if not tag_exists:
            tag_exists = Tag(tag=tag_content)
            db.session.add(tag_exists)
            db.session.commit()

        entry_tag = EntryTag(tag=tag_exists.id, entry=entry.id)
        db.session.add(entry_tag)

    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)