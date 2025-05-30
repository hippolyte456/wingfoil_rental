"""
Modèle de données pour le planning et les événements du calendrier.
"""

from datetime import datetime
from app import db

class CalendarEvent(db.Model):
    """Modèle pour représenter un événement dans le calendrier."""
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_type = db.Column(db.String(50), nullable=False, default='reservation')  # 'reservation', 'busy', 'holiday', etc.
    is_available = db.Column(db.Boolean, default=True)  # Indique si la plage horaire est disponible pour réservation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations avec les réservations et l'utilisateur admin
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=True)
    
    # Relations
    created_by = db.relationship('User', backref='created_events')
    reservation = db.relationship('Reservation', backref='calendar_event')
    
    def __repr__(self):
        return f'<CalendarEvent {self.title} ({self.start_time} - {self.end_time})>'
    
    @staticmethod
    def get_available_slots(start_date, end_date):
        """Récupère les créneaux disponibles entre deux dates."""
        return CalendarEvent.query.filter(
            CalendarEvent.start_time >= start_date,
            CalendarEvent.end_time <= end_date,
            CalendarEvent.is_available == True
        ).all()