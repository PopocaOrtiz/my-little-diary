from datetime import datetime
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

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
        entry = Entry(content=entry_content)
        try:
            db.session.add(entry)
            db.session.commit()
            return redirect('/entries')
        except Exception as ex:
            return f'An error has ocurred {ex}'
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


if __name__ == '__main__':
    app.run(debug=True)