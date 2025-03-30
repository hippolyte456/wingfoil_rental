from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import current_user, login_required
from ..models import Equipment, Reservation
from .. import db
from datetime import datetime
from .seo import generate_meta_tags, generate_structured_data, generate_breadcrumbs

bp = Blueprint('equipment', __name__)

@bp.route('/')
def equipment_list():
    equipment = Equipment.query.all()
    
    # Génération des meta tags
    meta_tags = generate_meta_tags(
        title="Location de Matériel Wingfoil",
        description="Découvrez notre sélection de matériel wingfoil à louer à Saint-Malo. Wings, foils et planches de qualité pour tous les niveaux.",
        image=url_for('static', filename='img/equipment/banner.jpg', _external=True)
    )
    
    # Génération des données structurées
    structured_data = generate_structured_data("LocalBusiness", {})
    
    # Génération des fils d'Ariane
    breadcrumbs = generate_breadcrumbs([
        {'name': 'Accueil', 'url': url_for('main.home')},
        {'name': 'Matériel', 'url': url_for('equipment.equipment_list')}
    ])
    
    return render_template(
        'equipment/index.html',
        equipment=equipment,
        meta_tags=meta_tags,
        structured_data=structured_data,
        breadcrumbs=breadcrumbs
    )

@bp.route('/<int:id>')
def equipment_detail(id):
    equipment = Equipment.query.get_or_404(id)
    
    # Génération des meta tags
    meta_tags = generate_meta_tags(
        title=f"{equipment.name} - Location Wingfoil",
        description=f"Louez {equipment.name} à Saint-Malo. {equipment.description[:150]}...",
        image=url_for('static', filename=equipment.image, _external=True),
        type='product'
    )
    
    # Génération des données structurées
    structured_data = generate_structured_data("Product", {
        'description': equipment.description,
        'image': url_for('static', filename=equipment.image, _external=True),
        'price': equipment.price_per_day
    })
    
    # Génération des fils d'Ariane
    breadcrumbs = generate_breadcrumbs([
        {'name': 'Accueil', 'url': url_for('main.home')},
        {'name': 'Matériel', 'url': url_for('equipment.equipment_list')},
        {'name': equipment.name, 'url': url_for('equipment.equipment_detail', id=equipment.id)}
    ])
    
    return render_template(
        'equipment/equipment_detail.html',
        equipment=equipment,
        meta_tags=meta_tags,
        structured_data=structured_data,
        breadcrumbs=breadcrumbs
    )

@bp.route('/reservation/<int:equipment_id>', methods=['GET', 'POST'])
@login_required
def make_reservation(equipment_id):
    equipment = Equipment.query.get_or_404(equipment_id)
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
            total_price=total_price
        )
        db.session.add(reservation)
        db.session.commit()
        flash('Réservation effectuée avec succès!', 'success')
        return redirect(url_for('equipment.my_reservations'))
    return render_template('reservations/make_reservation.html', equipment=equipment)

@bp.route('/my-reservations')
@login_required
def my_reservations():
    meta_tags = generate_meta_tags(
        title="Mes Réservations",
        description="Gérez vos réservations de matériel wingfoil."
    )
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('reservations/my_reservations.html', 
                         reservations=reservations,
                         meta_tags=meta_tags) 