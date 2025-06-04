"""
Vues pour l'interface d'administration de Wing4All.
Ces routes permettent aux administrateurs de gérer les utilisateurs, sites, équipements et réservations.
"""

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from . import bp
from app import db
from app.models.user import User
from app.models.site import Site
from app.models.equipment import Equipment
from app.models.reservation import Reservation
from app.models.calendar import CalendarEvent
from werkzeug.security import generate_password_hash
from functools import wraps
import datetime

def admin_required(f):
    """Décorateur pour restreindre l'accès aux administrateurs uniquement"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Accès restreint aux administrateurs.", "danger")
            return redirect(url_for('main.franchise'))
        return f(*args, **kwargs)
    return decorated_function

# Dashboard principal
@bp.route('/')
@login_required
@admin_required
def dashboard():
    """Page d'accueil de l'administration"""
    # Statistiques pour le tableau de bord
    stats = {
        'users_count': User.query.count(),
        'sites_count': Site.query.count(),
        'equipment_count': Equipment.query.count(),
        'reservations_count': Reservation.query.count(),
        'pending_reservations': Reservation.query.filter_by(status='pending').count()
    }
    return render_template('admin/dashboard.html', stats=stats)

# Gestion des utilisateurs
@bp.route('/users')
@login_required
@admin_required
def users_list():
    """Liste de tous les utilisateurs"""
    users = User.query.all()
    return render_template('admin/users/list.html', users=users)

@bp.route('/users/new', methods=['GET', 'POST'])
@login_required
@admin_required
def user_create():
    """Création d'un nouvel utilisateur"""
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        is_admin = 'is_admin' in request.form
        
        # Vérifier si l'e-mail existe déjà
        if User.query.filter_by(email=email).first():
            flash('Un utilisateur avec cet e-mail existe déjà.', 'danger')
            return redirect(url_for('admin.user_create'))
        
        user = User(
            email=email,
            name=name,
            password=generate_password_hash(password),
            is_admin=is_admin
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Utilisateur créé avec succès!', 'success')
        return redirect(url_for('admin.users_list'))
    
    return render_template('admin/users/create.html')

@bp.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(user_id):
    """Édition d'un utilisateur"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.email = request.form.get('email')
        user.name = request.form.get('name')
        user.is_admin = 'is_admin' in request.form
        
        # Mise à jour du mot de passe uniquement s'il est fourni
        password = request.form.get('password')
        if password and password.strip():
            user.password = generate_password_hash(password)
        
        db.session.commit()
        flash('Utilisateur mis à jour avec succès!', 'success')
        return redirect(url_for('admin.users_list'))
    
    return render_template('admin/users/edit.html', user=user)

@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def user_delete(user_id):
    """Suppression d'un utilisateur"""
    user = User.query.get_or_404(user_id)
    
    # Ne pas supprimer l'utilisateur actuellement connecté
    if user.id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte.', 'danger')
        return redirect(url_for('admin.users_list'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès!', 'success')
    return redirect(url_for('admin.users_list'))

# API pour les statistiques du tableau de bord
@bp.route('/api/stats')
@login_required
@admin_required
def get_stats():
    """API pour obtenir les statistiques actualisées"""
    stats = {
        'users_count': User.query.count(),
        'sites_count': Site.query.count(),
        'equipment_count': Equipment.query.count(),
        'reservations_count': Reservation.query.count(),
        'pending_reservations': Reservation.query.filter_by(status='pending').count()
    }
    return jsonify(stats)