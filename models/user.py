from multiprocessing.sharedctypes import Value
from tokenize import String
from app import db


class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(String(80), nullable=False)