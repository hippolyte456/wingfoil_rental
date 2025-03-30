from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'

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
    
    # Import et enregistrement des routes
    from .routes.seo import bp as seo_bp
    app.register_blueprint(seo_bp)
    
    with app.app_context():
        db.create_all()
    
    return app
