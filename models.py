from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    date = db.Column(db.String(50))
    venue = db.Column(db.String(100))
    source = db.Column(db.String(200))

    __table_args__ = (
        UniqueConstraint('title', 'date', 'venue', name='unique_event'),
    )