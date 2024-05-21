# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complain = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200))
    status = db.Column(db.String(50), nullable=False, default='offen')
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tickets = db.relationship('Ticket', backref='user', lazy=True)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tickets = db.relationship('Ticket', backref='customer', lazy=True)