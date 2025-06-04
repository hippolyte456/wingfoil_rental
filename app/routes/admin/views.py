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

# Gestion des sites
@bp.route('/sites')
@login_required
@admin_required
def sites_list():
    """Liste de tous les sites"""
    sites = Site.query.all()
    return render_template('admin/sites/list.html', sites=sites)

@bp.route('/sites/new', methods=['GET', 'POST'])
@login_required
@admin_required
def site_create():
    """Création d'un nouveau site"""
    if request.method == 'POST':
        # Récupération des données du formulaire
        name = request.form.get('name')
        slug = request.form.get('slug')
        description = request.form.get('description')
        address = request.form.get('address')
        postal_code = request.form.get('postal_code')
        city = request.form.get('city')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        phone = request.form.get('phone')
        email = request.form.get('email')
        is_active = 'is_active' in request.form
        
        # Vérifier si le slug existe déjà
        if Site.query.filter_by(slug=slug).first():
            flash('Un site avec ce slug existe déjà.', 'danger')
            return redirect(url_for('admin.site_create'))
        
        # Création du site
        site = Site(
            name=name,
            slug=slug,
            description=description,
            address=address,
            postal_code=postal_code,
            city=city,
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            phone=phone,
            email=email,
            is_active=is_active
        )
        db.session.add(site)
        db.session.commit()
        
        flash('Site créé avec succès!', 'success')
        return redirect(url_for('admin.sites_list'))
    
    return render_template('admin/sites/create.html')

@bp.route('/sites/<int:site_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def site_edit(site_id):
    """Édition d'un site"""
    site = Site.query.get_or_404(site_id)
    
    if request.method == 'POST':
        site.name = request.form.get('name')
        site.description = request.form.get('description')
        site.address = request.form.get('address')
        site.postal_code = request.form.get('postal_code')
        site.city = request.form.get('city')
        site.latitude = float(request.form.get('latitude')) if request.form.get('latitude') else None
        site.longitude = float(request.form.get('longitude')) if request.form.get('longitude') else None
        site.phone = request.form.get('phone')
        site.email = request.form.get('email')
        site.is_active = 'is_active' in request.form
        
        # Mise à jour du slug uniquement s'il est différent et n'existe pas déjà
        new_slug = request.form.get('slug')
        if new_slug != site.slug:
            if Site.query.filter_by(slug=new_slug).first():
                flash('Un site avec ce slug existe déjà.', 'danger')
                return render_template('admin/sites/edit.html', site=site)
            site.slug = new_slug
        
        db.session.commit()
        flash('Site mis à jour avec succès!', 'success')
        return redirect(url_for('admin.sites_list'))
    
    return render_template('admin/sites/edit.html', site=site)

@bp.route('/sites/<int:site_id>/delete', methods=['POST'])
@login_required
@admin_required
def site_delete(site_id):
    """Suppression d'un site"""
    site = Site.query.get_or_404(site_id)
    
    # Vérifier si le site a des équipements associés
    if site.equipment:
        flash('Ce site ne peut pas être supprimé car il contient des équipements.', 'danger')
        return redirect(url_for('admin.sites_list'))
    
    db.session.delete(site)
    db.session.commit()
    flash('Site supprimé avec succès!', 'success')
    return redirect(url_for('admin.sites_list'))

# Gestion des équipements
@bp.route('/equipment')
@login_required
@admin_required
def equipment_list():
    """Liste de tous les équipements"""
    equipment = Equipment.query.all()
    return render_template('admin/equipment/list.html', equipment=equipment)

@bp.route('/equipment/new', methods=['GET', 'POST'])
@login_required
@admin_required
def equipment_create():
    """Création d'un nouvel équipement"""
    sites = Site.query.all()
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        name = request.form.get('name')
        type = request.form.get('type')
        description = request.form.get('description')
        size = request.form.get('size')
        price_per_day = request.form.get('price_per_day')
        available = 'available' in request.form
        image_url = request.form.get('image_url')
        site_id = request.form.get('site_id')
        
        # Création de l'équipement
        equipment = Equipment(
            name=name,
            type=type,
            description=description,
            size=size,
            price_per_day=float(price_per_day) if price_per_day else 0,
            available=available,
            image_url=image_url,
            site_id=int(site_id) if site_id else None
        )
        db.session.add(equipment)
        db.session.commit()
        
        flash('Équipement créé avec succès!', 'success')
        return redirect(url_for('admin.equipment_list'))
    
    return render_template('admin/equipment/create.html', sites=sites)

@bp.route('/equipment/<int:equipment_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def equipment_edit(equipment_id):
    """Édition d'un équipement"""
    equipment = Equipment.query.get_or_404(equipment_id)
    sites = Site.query.all()
    
    if request.method == 'POST':
        equipment.name = request.form.get('name')
        equipment.type = request.form.get('type')
        equipment.description = request.form.get('description')
        equipment.size = request.form.get('size')
        equipment.price_per_day = float(request.form.get('price_per_day')) if request.form.get('price_per_day') else 0
        equipment.available = 'available' in request.form
        equipment.image_url = request.form.get('image_url')
        equipment.site_id = int(request.form.get('site_id')) if request.form.get('site_id') else None
        
        db.session.commit()
        flash('Équipement mis à jour avec succès!', 'success')
        return redirect(url_for('admin.equipment_list'))
    
    return render_template('admin/equipment/edit.html', equipment=equipment, sites=sites)

@bp.route('/equipment/<int:equipment_id>/delete', methods=['POST'])
@login_required
@admin_required
def equipment_delete(equipment_id):
    """Suppression d'un équipement"""
    equipment = Equipment.query.get_or_404(equipment_id)
    
    # Vérifier si l'équipement a des réservations
    if equipment.reservations:
        flash('Cet équipement ne peut pas être supprimé car il a des réservations associées.', 'danger')
        return redirect(url_for('admin.equipment_list'))
    
    db.session.delete(equipment)
    db.session.commit()
    flash('Équipement supprimé avec succès!', 'success')
    return redirect(url_for('admin.equipment_list'))

# Gestion des réservations
@bp.route('/reservations')
@login_required
@admin_required
def reservations_list():
    """Liste de toutes les réservations"""
    reservations = Reservation.query.all()
    return render_template('admin/reservations/list.html', reservations=reservations)

@bp.route('/reservations/new', methods=['GET', 'POST'])
@login_required
@admin_required
def reservation_create():
    """Création d'une nouvelle réservation"""
    users = User.query.all()
    equipment = Equipment.query.all()
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        user_id = request.form.get('user_id')
        equipment_id = request.form.get('equipment_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        total_price = request.form.get('total_price')
        status = request.form.get('status')
        
        # Conversion des dates
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Création de la réservation
        reservation = Reservation(
            user_id=int(user_id),
            equipment_id=int(equipment_id),
            start_date=start_date,
            end_date=end_date,
            total_price=float(total_price) if total_price else 0,
            status=status
        )
        db.session.add(reservation)
        db.session.commit()
        
        flash('Réservation créée avec succès!', 'success')
        return redirect(url_for('admin.reservations_list'))
    
    return render_template('admin/reservations/create.html', users=users, equipment=equipment)

@bp.route('/reservations/<int:reservation_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def reservation_edit(reservation_id):
    """Édition d'une réservation"""
    reservation = Reservation.query.get_or_404(reservation_id)
    users = User.query.all()
    equipment = Equipment.query.all()
    
    if request.method == 'POST':
        reservation.user_id = int(request.form.get('user_id'))
        reservation.equipment_id = int(request.form.get('equipment_id'))
        reservation.start_date = datetime.datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        reservation.end_date = datetime.datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        reservation.total_price = float(request.form.get('total_price')) if request.form.get('total_price') else 0
        reservation.status = request.form.get('status')
        
        db.session.commit()
        flash('Réservation mise à jour avec succès!', 'success')
        return redirect(url_for('admin.reservations_list'))
    
    return render_template('admin/reservations/edit.html', reservation=reservation, users=users, equipment=equipment)

@bp.route('/reservations/<int:reservation_id>/delete', methods=['POST'])
@login_required
@admin_required
def reservation_delete(reservation_id):
    """Suppression d'une réservation"""
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Réservation supprimée avec succès!', 'success')
    return redirect(url_for('admin.reservations_list'))

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