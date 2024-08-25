from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime, default=func.now())
    taken = db.Column(db.Boolean, default=False)
    taken_by = db.Column(db.String(500), default='')
    points = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    points = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    is_allowed = db.Column(db.Boolean, default=True)
    login_dates = db.Column(db.JSON, default=list)
    data = db.Column(db.String, default="")
    tasks_complete = db.Column(db.String, default="")
