#!/usr/bin/env python3
"""
Script d'initialisation de la base de données PostgreSQL pour Wing4All.
Ce script crée toutes les tables nécessaires et un utilisateur admin par défaut.
"""

import os
import sys
import getpass

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.site import Site
from app.models.equipment import Equipment
from app.models.reservation import Reservation
from app.models.calendar import CalendarEvent
from werkzeug.security import generate_password_hash

def init_database():
    """Initialise la base de données avec les tables et un utilisateur admin"""
    print("=== Initialisation de la base de données Wing4All ===")
    print("Ce script va créer une nouvelle base de données pour l'application Wing4All.")
    
    # Créer l'application avec la configuration de développement
    print("Création de l'application Flask avec la configuration de développement...")
    app = create_app('development')
    
    with app.app_context():
        # Création des tables
        print("Création des tables dans la base de données PostgreSQL...")
        db.drop_all()  # Supprimer les tables existantes
        db.create_all()  # Créer de nouvelles tables
        
        # Création d'un utilisateur administrateur
        print("\n=== Création d'un utilisateur administrateur ===")
        admin_email = input("Email de l'administrateur [admin@wing4all.fr]: ") or "admin@wing4all.fr"
        admin_name = input("Nom de l'administrateur [Admin Wing4All]: ") or "Admin Wing4All"
        admin_password = getpass.getpass("Mot de passe de l'administrateur [admin123]: ") or "admin123"
        
        admin = User(
            email=admin_email,
            name=admin_name,
            password=generate_password_hash(admin_password),
            is_admin=True
        )
        
        # Création d'un utilisateur gestionnaire de site
        manager = User(
            email="manager@wing4all.fr",
            name="Gestionnaire Site",
            password=generate_password_hash("manager123"),
            is_admin=False  # Pas admin mais gestionnaire de site (à gérer dans l'interface)
        )
        
        # Création d'un utilisateur client
        client = User(
            email="client@example.com",
            name="Client Test",
            password=generate_password_hash("client123"),
            is_admin=False
        )
        
        # Ajout d'un site de démonstration
        demo_site = Site(
            name="Wing4All Saint-Malo",
            slug="saint-malo",
            description="Centre de wingfoil situé à Saint-Malo, idéal pour profiter des conditions exceptionnelles de vent et de mer.",
            address="1 Plage du Sillon",
            postal_code="35400",
            city="Saint-Malo",
            latitude=48.6520,
            longitude=-2.0067,
            phone="06 12 34 56 78",
            email="saintmalo@wing4all.fr",
            is_active=True
        )
        
        # Ajout à la session
        db.session.add(admin)
        db.session.add(manager)
        db.session.add(client)
        db.session.add(demo_site)
        
        # Commit des changements
        db.session.commit()
        
        # Ajout d'équipements
        site_id = demo_site.id
        equipments = [
            {
                "name": "Wing Gong 4m²",
                "type": "Wing",
                "description": "Wing Gong 4m² idéale pour vents moyens à forts",
                "size": "4m²",
                "price_per_day": 40.0,
                "available": True,
                "image_url": "img/equipment/wing_takoon.png",
                "site_id": site_id
            },
            {
                "name": "Planche Gong 120L",
                "type": "Planche",
                "description": "Planche stable pour débutants et intermédiaires",
                "size": "120L",
                "price_per_day": 50.0,
                "available": True,
                "image_url": "img/equipment/board_hype.png",
                "site_id": site_id
            },
            {
                "name": "Foil Gong Allvator",
                "type": "Foil",
                "description": "Foil polyvalent pour tous niveaux",
                "size": "",
                "price_per_day": 60.0,
                "available": True,
                "image_url": "img/equipment/foil_gong_1550.jpeg",
                "site_id": site_id
            }
        ]
        
        # Ajout des équipements à la base de données
        for equip_data in equipments:
            equipment = Equipment(**equip_data)
            db.session.add(equipment)
        
        # Commit des équipements
        db.session.commit()
        
        print("\n=== Base de données initialisée avec succès ===")
        print(f"Utilisateur admin créé: {admin_email}")
        print("Vous pouvez maintenant démarrer votre application Flask et vous connecter avec ces identifiants.")

if __name__ == "__main__":
    init_database()