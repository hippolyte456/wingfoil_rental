#!/usr/bin/env python3
"""
Script pour ajouter des sites à Fréjus et La Baule dans la base de données Wing4All.
Exécuter depuis le répertoire racine avec: python scripts/add_sites.py
"""

import os
import sys
from pathlib import Path

# Ajout du répertoire parent au path pour importer l'application
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app, db
from app.models.site import Site

def add_sites():
    """Ajoute les sites de Fréjus et La Baule à la base de données"""
    
    # Création des objets Site
    frejus = Site(
        name="Wing4All Fréjus",
        slug="frejus",
        description="Découvrez le wingfoil dans un cadre exceptionnel sur la côte méditerranéenne. "
                   "Notre centre Wing4All à Fréjus vous accueille toute l'année avec des conditions "
                   "idéales pour l'apprentissage et la pratique du wingfoil.",
        address="Plage de la Base Nature",
        postal_code="83600",
        city="Fréjus",
        latitude=43.4178,
        longitude=6.7503,
        phone="04.94.51.XX.XX",
        email="frejus@wing4all.fr",
        is_active=True
    )
    
    la_baule = Site(
        name="Wing4All La Baule",
        slug="la-baule",
        description="Notre centre Wing4All à La Baule vous propose une expérience unique de wingfoil "
                   "sur la magnifique baie de La Baule. Profitez de nos cours et de notre matériel "
                   "haut de gamme dans un environnement idéal pour tous les niveaux.",
        address="Plage Benoît",
        postal_code="44500",
        city="La Baule-Escoublac",
        latitude=47.2833,
        longitude=-2.3953,
        phone="02.40.60.XX.XX",
        email="labaule@wing4all.fr",
        is_active=True
    )
    
    # Vérification si les sites existent déjà
    existing_frejus = Site.query.filter_by(slug="frejus").first()
    existing_la_baule = Site.query.filter_by(slug="la-baule").first()
    
    # Ajout des sites s'ils n'existent pas déjà
    sites_added = 0
    
    if not existing_frejus:
        db.session.add(frejus)
        print(f"Site ajouté: {frejus.name}")
        sites_added += 1
    else:
        print(f"Le site {frejus.name} existe déjà.")
    
    if not existing_la_baule:
        db.session.add(la_baule)
        print(f"Site ajouté: {la_baule.name}")
        sites_added += 1
    else:
        print(f"Le site {la_baule.name} existe déjà.")
    
    # Commit des changements
    if sites_added > 0:
        db.session.commit()
        print(f"{sites_added} site(s) ajouté(s) avec succès!")
    else:
        print("Aucun nouveau site n'a été ajouté.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        add_sites()