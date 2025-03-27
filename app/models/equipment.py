from app import db

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # wing, board, foil
    description = db.Column(db.Text)
    size = db.Column(db.String(20))
    price_per_day = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(200))
    reservations = db.relationship('Reservation', backref='equipment', lazy=True) 