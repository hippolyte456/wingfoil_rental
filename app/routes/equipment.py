from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import current_user, login_required
from ..models import Equipment, Reservation
from ..models.site import Site
from .. import db
from datetime import datetime
from .seo import generate_meta_tags, generate_structured_data, generate_breadcrumbs

bp = Blueprint('equipment', __name__)

@bp.route('/site/<site_slug>/equipment')
def equipment_list(site_slug=None):
    site = None
    if site_slug:
        site = Site.query.filter_by(slug=site_slug).first_or_404()
        # Filtrer les équipements par site
        equipment = Equipment.query.filter_by(site_id=site.id).all()
        city_name = site.city
    else:
        # Tous les équipements si aucun site spécifié
        equipment = Equipment.query.all()
        city_name = "nos sites"
    
    # Génération des meta tags
    meta_tags = generate_meta_tags(
        title=f"Location de Matériel Wingfoil à {city_name}",
        description=f"Découvrez notre sélection de matériel wingfoil à louer à {city_name}. Wings, foils et planches de qualité pour tous les niveaux.",
        image=url_for('static', filename='img/equipment/banner.jpg', _external=True)
    )
    
    # Génération des données structurées
    structured_data = generate_structured_data("LocalBusiness", {})
    
    # Génération des fils d'Ariane
    if site:
        breadcrumbs = generate_breadcrumbs([
            {'name': 'Réseau Wing4All', 'url': url_for('main.franchise')},
            {'name': site.city, 'url': url_for('main.site_home', site_slug=site.slug)},
            {'name': 'Matériel', 'url': url_for('equipment.equipment_list', site_slug=site.slug)}
        ])
    else:
        breadcrumbs = generate_breadcrumbs([
            {'name': 'Accueil', 'url': url_for('main.franchise')},
            {'name': 'Matériel', 'url': url_for('equipment.equipment_list')}
        ])
    
    return render_template(
        'sites/equipment/index.html',
        equipment=equipment,
        meta_tags=meta_tags,
        structured_data=structured_data,
        breadcrumbs=breadcrumbs,
        site=site
    )

@bp.route('/')
def equipment_list_all():
    return equipment_list()

@bp.route('/site/<site_slug>/equipment/<int:id>')
def equipment_detail(id, site_slug=None):
    equipment = Equipment.query.get_or_404(id)
    
    site = None
    if site_slug:
        site = Site.query.filter_by(slug=site_slug).first_or_404()
        # Vérifier que l'équipement appartient au site
        if equipment.site_id != site.id:
            flash("Ce matériel n'est pas disponible sur ce site.", "warning")
            return redirect(url_for('equipment.equipment_list', site_slug=site_slug))
    
    # Génération des meta tags
    meta_tags = generate_meta_tags(
        title=f"{equipment.name} - Location Wingfoil",
        description=f"Louez {equipment.name} à {site.city if site else 'Wing4All'}. {equipment.description[:150]}...",
        image=url_for('static', filename=equipment.image_url, _external=True),
        type='product'
    )
    
    # Génération des données structurées
    structured_data = generate_structured_data("Product", {
        'description': equipment.description,
        'image': url_for('static', filename=equipment.image_url, _external=True),
        'price': equipment.price_per_day
    })
    
    # Génération des fils d'Ariane
    if site:
        breadcrumbs = generate_breadcrumbs([
            {'name': 'Réseau Wing4All', 'url': url_for('main.franchise')},
            {'name': site.city, 'url': url_for('main.site_home', site_slug=site.slug)},
            {'name': 'Matériel', 'url': url_for('equipment.equipment_list', site_slug=site.slug)},
            {'name': equipment.name, 'url': url_for('equipment.equipment_detail', id=equipment.id, site_slug=site.slug)}
        ])
    else:
        breadcrumbs = generate_breadcrumbs([
            {'name': 'Accueil', 'url': url_for('main.franchise')},
            {'name': 'Matériel', 'url': url_for('equipment.equipment_list')},
            {'name': equipment.name, 'url': url_for('equipment.equipment_detail', id=equipment.id)}
        ])
    
    return render_template(
        'sites/equipment/equipment_detail.html',
        equipment=equipment,
        meta_tags=meta_tags,
        structured_data=structured_data,
        breadcrumbs=breadcrumbs,
        site=site
    )

@bp.route('/<int:id>')
def equipment_detail_all(id):
    return equipment_detail(id)

@bp.route('/site/<site_slug>/reservation/<int:equipment_id>', methods=['GET', 'POST'])
@login_required
def make_reservation(equipment_id, site_slug=None):
    equipment = Equipment.query.get_or_404(equipment_id)
    
    site = None
    if site_slug:
        site = Site.query.filter_by(slug=site_slug).first_or_404()
        # Vérifier que l'équipement appartient au site
        if equipment.site_id != site.id:
            flash("Ce matériel n'est pas disponible sur ce site.", "warning")
            return redirect(url_for('equipment.equipment_list', site_slug=site_slug))
    
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        days = (end_date - start_date).days
        total_price = days * equipment.price_per_day
        
        reservation = Reservation(
            user_id=current_user.id,
            equipment_id=equipment_id,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            site_id=site.id if site else None
        )
        db.session.add(reservation)
        db.session.commit()
        flash('Réservation effectuée avec succès!', 'success')
        return redirect(url_for('equipment.my_reservations'))
        
    return render_template('sites/equipment/make_reservation.html', equipment=equipment, site=site)

@bp.route('/reservation/<int:equipment_id>', methods=['GET', 'POST'])
@login_required
def make_reservation_all(equipment_id):
    return make_reservation(equipment_id)

@bp.route('/my-reservations')
@login_required
def my_reservations():
    meta_tags = generate_meta_tags(
        title="Mes Réservations",
        description="Gérez vos réservations de matériel wingfoil."
    )
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    
    # Récupérer les détails du site pour chaque réservation
    for reservation in reservations:
        if reservation.site_id:
            reservation.site = Site.query.get(reservation.site_id)
        else:
            reservation.site = None
    
    return render_template(
        'sites/equipment/my_reservations.html', 
        reservations=reservations,
        meta_tags=meta_tags,
        site=None  # Pas de site spécifique pour cette page
    )