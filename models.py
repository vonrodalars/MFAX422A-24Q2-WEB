# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beschwerde = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='offen')
    erstellungsdatum = db.Column(db.DateTime, nullable=False, default=db.func.now())
    bearbeiter_id = db.Column(db.Integer, db.ForeignKey('bearbeiter.id'))

class Bearbeiter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tickets = db.relationship('Ticket', backref='bearbeiter', lazy=True)
