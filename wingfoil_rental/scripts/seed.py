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
            {
                'name': 'Duotone Unit Wing 5m',
                'description': 'Aile de wingfoil polyvalente, parfaite pour débuter et progresser. Excellente stabilité et facilité de prise en main.',
                'type': 'wing',
                'size': '5m',
                'price_per_day': 45,
                'available': True,
                'image_url': 'img/equipment/test.png'
            },
            {
                'name': 'F-One Strike 4m',
                'description': 'Aile compacte et légère, idéale pour les vents forts. Grande plage d\'utilisation.',
                'type': 'wing',
                'size': '4m',
                'price_per_day': 40,
                'available': True,
                'image_url': 'img/equipment/test.png'
            },
            {
                'name': 'Fanatic Sky Wing 150L',
                'description': 'Board stable et polyvalente, parfaite pour l\'apprentissage et la progression.',
                'type': 'board',
                'size': '150L',
                'price_per_day': 55,
                'available': True,
                'image_url': 'img/equipment/test.png'
            },
            {
                'name': 'Starboard Hyperfoil 95L',
                'description': 'Board compacte pour riders avancés, très réactive et maniable.',
                'type': 'board',
                'size': '95L',
                'price_per_day': 60,
                'available': True,
                'image_url': 'img/equipment/test.png'
            },
            {
                'name': 'GoFoil Iwa',
                'description': 'Foil polyvalent, stable et progressif. Idéal pour débuter et progresser.',
                'type': 'foil',
                'size': 'M',
                'price_per_day': 65,
                'available': True,
                'image_url': 'img/equipment/test.png'
            }
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