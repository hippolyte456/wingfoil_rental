from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app('development')

with app.app_context():
    # Vérifier si l'utilisateur existe déjà
    admin_email = "nouvel_admin@wing4all.fr"
    existing_user = User.query.filter_by(email=admin_email).first()
    
    if existing_user:
        # Mettre à jour le mot de passe
        existing_user.password = generate_password_hash("admin123456")
        existing_user.is_admin = True
        print(f"Utilisateur {admin_email} mis à jour avec le nouveau mot de passe.")
    else:
        # Créer un nouvel utilisateur administrateur
        new_admin = User(
            email=admin_email,
            name="Nouvel Admin",
            password=generate_password_hash("admin123456"),
            is_admin=True
        )
        db.session.add(new_admin)
        print(f"Utilisateur {admin_email} créé.")
    
    db.session.commit()
    print("Opération terminée avec succès.")