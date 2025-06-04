from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from .models import user, equipment, reservation
    
    # Import et enregistrement des blueprints
    from .routes.main import bp as main_bp
    from .routes.auth import bp as auth_bp
    from .routes.equipment import bp as equipment_bp
    from .routes.seo import bp as seo_bp
    from .routes.admin import bp as admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(equipment_bp, url_prefix='/equipment')
    app.register_blueprint(seo_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Accès aux constantes LOGO_PATH et CONTACT_EMAIL dans les templates
    @app.context_processor
    def inject_constants():
        return {
            "LOGO_PATH": app.config.get('LOGO_PATH', 'img/logo/logo_wingfoil-rm-bg.png'),
            "CONTACT_EMAIL": app.config.get('CONTACT_EMAIL', 'contact@wing4all.fr')
        }
    
    # Helper function to check if a file exists in static folder
    @app.context_processor
    def utility_processor():
        def file_exists(file_path):
            full_path = os.path.join(app.static_folder, file_path)
            return os.path.exists(full_path)
        return dict(file_exists=file_exists)
    
    with app.app_context():
        db.create_all()
    
    return app
