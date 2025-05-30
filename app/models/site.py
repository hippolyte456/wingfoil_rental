from app import db

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    postal_code = db.Column(db.String(20))
    city = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relations avec les autres modèles
    equipments = db.relationship('Equipment', backref='site', lazy=True)
    events = db.relationship('CalendarEvent', backref='site', lazy=True)
    
    def __repr__(self):
        return f"<Site {self.name}>"
    
    @property
    def map_info(self):
        """Retourne les informations pour l'affichage sur la carte"""
        return {
            'name': self.name,
            'slug': self.slug,
            'lat': self.latitude,
            'lng': self.longitude,
            'description': self.description
        }