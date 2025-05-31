import os
import sys

# Ajoute le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.equipment import Equipment
from app.models.user import User
from app.models.site import Site
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
        
        # Crée un site par défaut
        default_site = Site(
            name="Saint-Malo",
            slug="saint-malo",
            description="Centre de wingfoil Wing4All situé à Saint-Malo",
            address="Plage du Sillon",
            postal_code="35400",
            city="Saint-Malo",
            latitude=48.6520,
            longitude=-2.0067,
            phone="06 12 34 56 78",
            email="saintmalo@wing4all.fr",
            is_active=True
        )
        db.session.add(default_site)
        db.session.flush()  # Pour obtenir l'ID du site avant de l'utiliser

        # Liste des équipements de wingfoil
        equipments = [
            {"type": "Planche", "name": "gong 110L", "description": "", "size": "", 
             "price_per_day": 0, "available": True, "image_url": "img/equipment/board_hype.png", "site_id": default_site.id},
            {"type": "Planche", "name": "gong 130L", "description": "", "size": "",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/board_hype.png", "site_id": default_site.id},
            {"type": "Planche", "name": "AFS 90L", "description": "", "size": "",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/board_AFS.png", "site_id": default_site.id},
            {"type": "Planche", "name": "gong 80L", "description": "", "size": "",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/board_hype.png", "site_id": default_site.id},
            {"type": "Wing", "name": "Takoon 3m", "description": "", "size": "3m",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/wing_takoon.png", "site_id": default_site.id},
            {"type": "Wing", "name": "Zeeko 4m", "description": "", "size": "4m",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/wing_zeeko.png", "site_id": default_site.id},
            {"type": "Wing", "name": "Takoon 6m", "description": "", "size": "6m",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/wing_takoon.png", "site_id": default_site.id},
            {"type": "Wing", "name": "Swing 5m", "description": "", "size": "5m",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/wing_swing.png", "site_id": default_site.id},
            {"type": "Wing", "name": "Neutra 4m", "description": "", "size": "4m",
             "price_per_day": 0, "available": True, "image_url": "img/equipment/wing_takoon.png", "site_id": default_site.id},
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