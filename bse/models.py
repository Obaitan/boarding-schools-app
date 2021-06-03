from bse import db
from datetime import datetime


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    excerpt = db.Column(db.String(300), nullable=False, unique=True)
    article = db.Column(db.Text, nullable=False, unique=True)
    author = db.Column(db.String(40), nullable=False,
                       unique=True, default='Unknown')
    date = db.Column(db.DateTime, nullable=False,
                     unique=True, default=datetime.utcnow)
    thumbnail = db.Column(db.Text, nullable=False, unique=True)
    name = db.Column(db.Text, nullable=False,  unique=True)
    mimetype = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'News {self.name}'


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    flag = db.Column(db.Text, nullable=False, unique=True)
    mimetype = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'News {self.name}'
