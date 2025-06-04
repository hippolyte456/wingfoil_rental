from flask import Blueprint

# Création du blueprint pour l'administration
bp = Blueprint('admin', __name__, url_prefix='/admin')

from . import views  # Import des vues après la création du blueprint pour éviter les imports circulaires