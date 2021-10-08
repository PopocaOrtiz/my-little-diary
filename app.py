from datetime import datetime
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

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
            return f'entry {entry.id} created'
        except Exception as ex:
            return f'An error has ocurred {ex}'
    else:
        return render_template('entries.html')


if __name__ == '__main__':
    app.run(debug=True)