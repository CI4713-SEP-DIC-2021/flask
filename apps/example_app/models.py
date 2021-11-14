import os
from app import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    photo = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, name, photo, description):
        self.name = name
        self.photo = photo
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'photo':self.photo,
            'description':self.description,
        }