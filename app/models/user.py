from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Augmenté à 255 caractères pour accommoder les hash de mot de passe
    name = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Nouvel attribut pour les permissions admin
    reservations = db.relationship('Reservation', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'