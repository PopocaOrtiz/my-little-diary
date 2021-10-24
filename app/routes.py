from typing import Union

from flask import render_template, flash, redirect, Response, url_for, request
from flask_sqlalchemy import SQLAlchemy

from app import app
from app.forms import LoginForm
from entries import get_entries
from entries.models import Entry
from tags import detect_tags, get_tag
from tags.models import Tag, EntryTag

db = SQLAlchemy()


@app.route('/login', methods=['GET','POST'])
def login() -> Union[str, Response]:
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/')
def index() -> Response:
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


if __name__ == '__main__':
    app.run(debug=True)