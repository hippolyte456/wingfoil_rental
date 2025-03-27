import os
import sys

# Ajoute le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.equipment import Equipment
from app.models.user import User
from werkzeug.security import generate_password_hash

def seed_database():
    app = create_app()
    with app.app_context():
        # Supprime toutes les données existantes
        db.drop_all()
        db.create_all()

        # Crée un utilisateur admin
        admin = User(
            name='Admin User',
            email='admin@example.com',
            password=generate_password_hash('admin123')
        )
        db.session.add(admin)

        # Liste des équipements de wingfoil
        equipments = [
            {"type": "Planche", "name": "gong 110L", "description": "", "size": "", 
             "price_per_day": 0, "available": True, "image_url": "img/equipment/board_hype.png"},
            {"type": "Planche", "name": "gong 130L", "description": "", "size": "",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/board_hype.png"},
            {"type": "Planche", "name": "AFS 90L", "description": "", "size": "",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/board_AFS.png"},
            {"type": "Planche", "name": "gong 80L", "description": "", "size": "",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/board_hype.png"},
            {"type": "Wing", "name": "Takoon 3m", "description": "", "size": "3m",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/wing_takoon.png"},
            {"type": "Wing", "name": "Zeeko 4m", "description": "", "size": "4m",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/wing_zeeko.png"},
            {"type": "Wing", "name": "Takoon 6m", "description": "", "size": "6m",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/wing_takoon.png"},
            {"type": "Wing", "name": "Swing 5m", "description": "", "size": "5m",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/wing_swing.png"},
            {"type": "Wing", "name": "Neutra 4m", "description": "", "size": "4m",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/wing_takoon.png"},
        ]

        # Ajoute les équipements
        for equipment_data in equipments:
            equipment = Equipment(**equipment_data)
            db.session.add(equipment)

        # Commit les changements
        db.session.commit()

if __name__ == '__main__':
    seed_database()
    print("Base de données initialisée avec succès !") 