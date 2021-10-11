from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return f'<Tag {id}>'


class EntryTag(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Integer, nullable=False)
    entry = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<EntryTag {id}>'
