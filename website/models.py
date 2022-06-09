from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    textMessage = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    messages = db.relationship('Messages')