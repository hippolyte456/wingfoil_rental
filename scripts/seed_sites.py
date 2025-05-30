"""
Script pour ajouter les données initiales des sites Wing4All
"""

import sys
import os

# Ajouter le répertoire parent au chemin pour pouvoir importer les modules de l'application
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.site import Site

def seed_sites():
    """Ajoute les sites initiaux à la base de données"""
    # Création des sites
    sites = [
        Site(
            name="Saint-Malo",
            slug="saint-malo",
            description="Centre de wingfoil Wing4All situé à Saint-Malo, dans un cadre exceptionnel pour profiter des meilleures conditions de vent et de mer.",
            address="Plage du Sillon",
            postal_code="35400",
            city="Saint-Malo",
            latitude=48.6520,
            longitude=-2.0067,
            phone="06 12 34 56 78",
            email="saintmalo@wing4all.fr",
            is_active=True
        ),
        Site(
            name="Fréjus",
            slug="frejus",
            description="Le spot de wingfoil Wing4All de Fréjus vous accueille tout au long de l'année avec des conditions idéales pour la pratique dans le sud de la France.",
            address="Plage de Fréjus",
            postal_code="83600",
            city="Fréjus",
            latitude=43.4182,
            longitude=6.7372,
            phone="06 98 76 54 32",
            email="frejus@wing4all.fr",
            is_active=True
        ),
        Site(
            name="Leucate",
            slug="leucate",
            description="Spot de wingfoil Wing4All situé dans l'Aude, connu pour ses conditions de vent exceptionnelles et son plan d'eau adapté à tous les niveaux.",
            address="Port Leucate",
            postal_code="11370",
            city="Leucate",
            latitude=42.9421,
            longitude=3.0555,
            phone="06 45 67 89 01",
            email="leucate@wing4all.fr",
            is_active=True
        )
    ]
    
    # Ajout des sites à la base de données
    for site in sites:
        # Vérifier si le site existe déjà
        existing = Site.query.filter_by(slug=site.slug).first()
        if not existing:
            db.session.add(site)
    
    # Validation des changements
    db.session.commit()
    print(f"✅ {len(sites)} sites ajoutés avec succès")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_sites()