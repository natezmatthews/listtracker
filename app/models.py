from datetime import datetime
from app import db

class Risuto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True)
    description = db.Column(db.String(280))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    separators = db.relationship('Separator', backref='risuto', lazy='dynamic')
    items = db.relationship('Item', backref='risuto', lazy='dynamic')

    def __repr__(self):
        return '<Risuto {}>'.format(self.name)

class Separator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    separator = db.Column(db.String(5), unique=True)
    risuto_id = db.Column(db.Integer, db.ForeignKey('risuto.id'))

    def __repr__(self):
        return '<Separator {}>'.format(self.separator)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80))
    risuto_id = db.Column(db.Integer, db.ForeignKey('risuto.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.item)