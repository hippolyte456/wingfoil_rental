from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .seo import generate_meta_tags, generate_structured_data
from flask_login import current_user, login_required
from app.models.calendar import CalendarEvent
from app.models.article import get_sorted_articles, get_article_by_slug
from app.models.site import Site
from app import db
from datetime import datetime, timedelta
import json

bp = Blueprint('main', __name__)

# Routes du site parent (franchise)
@bp.route('/')
def franchise():
    meta_tags = generate_meta_tags(
        title="Wing4All - Réseau de location de Wingfoil en France",
        description="Découvrez le réseau Wing4All de location de matériel de wingfoil en France. Plusieurs sites pour vous accompagner dans votre pratique du wingfoil."
    )
    structured_data = generate_structured_data("Organization", {})
    
    return render_template('franchise/home_franchise.html', 
                          meta_tags=meta_tags, 
                          structured_data=structured_data)

@bp.route('/reseau')
def reseau():
    meta_tags = generate_meta_tags(
        title="Notre réseau d'écoles de wingfoil - Wing4All",
        description="Découvrez tous nos points de location de matériel de wingfoil en France. Plusieurs sites idéalement situés pour votre pratique du wingfoil."
    )
    structured_data = generate_structured_data("Organization", {})
    
    # Récupérer tous les sites actifs
    sites = Site.query.filter_by(is_active=True).all()
    
    # Vérifier que chaque site a des coordonnées valides pour la carte
    valid_sites = []
    for site in sites:
        if site.latitude is not None and site.longitude is not None:
            valid_sites.append(site)
        else:
            print(f"Warning: Site {site.name} missing coordinates")
    
    # Préparer les données JSON pour la carte
    sites_json = json.dumps([{
        'name': site.name,
        'slug': site.slug,
        'lat': float(site.latitude),  # Convertir explicitement en float pour JSON
        'lng': float(site.longitude), # Convertir explicitement en float pour JSON
        'description': site.description
    } for site in valid_sites])
    
    # Afficher les coordonnées pour le débogage
    for site in valid_sites:
        print(f"DEBUG - Site: {site.name}, Lat: {site.latitude}, Lng: {site.longitude}")
        
    return render_template('franchise/reseau.html', 
                          meta_tags=meta_tags, 
                          structured_data=structured_data,
                          sites=sites,
                          sites_json=sites_json)

# Route maintenue pour la compatibilité avec les références existantes
@bp.route('/home')
def home():
    return redirect(url_for('main.franchise'))

@bp.route('/actualites')
def actualites():
    meta_tags = generate_meta_tags(
        title="Actualités Wing4All",
        description="Suivez toutes les actualités de Wing4All : événements, nouveautés, promotions et informations sur la location de matériel de wingfoil."
    )
    # Récupérer les articles triés du plus récent au plus ancien
    articles = get_sorted_articles(reverse=True)
    return render_template('franchise/actualites.html', 
                          meta_tags=meta_tags, 
                          articles=articles)

@bp.route('/conseils')
def conseils():
    meta_tags = generate_meta_tags(
        title="Conseils Wingfoil",
        description="Conseils et astuces pour la pratique du wingfoil. Apprenez avec nos moniteurs FFV diplômés qui optimisent votre courbe d'apprentissage."
    )
    return render_template('franchise/conseils.html', 
                          meta_tags=meta_tags)

# Routes des sites enfants
@bp.route('/site/<site_slug>')
def site_home(site_slug):
    # Récupérer le site correspondant au slug
    site = Site.query.filter_by(slug=site_slug).first_or_404()
    
    meta_tags = generate_meta_tags(
        title=f"Location de Wingfoil à {site.city} - {site.name}",
        description=f"Location de matériel de wingfoil à {site.city}. Wings, foils et planches de qualité pour tous les niveaux. Conseils et accompagnement personnalisé."
    )
    structured_data = generate_structured_data("LocalBusiness", {})
    return render_template('sites/home.html', 
                           meta_tags=meta_tags, 
                           structured_data=structured_data, 
                           site=site)

@bp.route('/site/<site_slug>/formules')
def formules(site_slug=None):
    site = None
    if site_slug:
        site = Site.query.filter_by(slug=site_slug).first_or_404()
        city_name = site.city
    else:
        city_name = "nos sites"
    
    meta_tags = generate_meta_tags(
        title=f"Formules Location Wingfoil",
        description=f"Découvrez nos formules de location de matériel wingfoil à {city_name}. Prix attractifs et matériel de qualité pour tous les niveaux."
    )
    return render_template('sites/formules.html', meta_tags=meta_tags, site=site)

@bp.route('/site/<site_slug>/events')
def events(site_slug=None):
    site = None
    if site_slug:
        site = Site.query.filter_by(slug=site_slug).first_or_404()
        city_name = site.city
    else:
        city_name = "nos sites"
    
    meta_tags = generate_meta_tags(
        title=f"Événements Wingfoil - Wing4All {city_name}",
        description=f"Découvrez les événements wingfoil organisés à {city_name}. Initiations, compétitions et rencontres autour de la pratique du wingfoil."
    )
    # Récupérer les prochains événements
    now = datetime.now()
    
    # ⚠️ Modification: Ne pas filtrer par site_id pour l'instant, car cette colonne n'existe pas dans la base
    # Nous récupérons tous les événements et filtrons manuellement après si nécessaire
    upcoming_events = CalendarEvent.query.filter(
        CalendarEvent.start_time >= now,
        CalendarEvent.event_type == 'event'
    ).order_by(CalendarEvent.start_time).limit(30).all()
    
    # Si un site est spécifié, on pourrait filtrer manuellement les événements ici ultérieurement
    # Pour l'instant, on affiche tous les événements pour chaque site
    
    return render_template('sites/events.html', meta_tags=meta_tags, events=upcoming_events, site=site)

@bp.route('/site/<site_slug>/planning')
def planning(site_slug=None):
    site = None
    if site_slug:
        site = Site.query.filter_by(slug=site_slug).first_or_404()
        city_name = site.city
    else:
        city_name = "nos sites"
    
    meta_tags = generate_meta_tags(
        title=f"Planning et Disponibilités - {city_name}",
        description=f"Consultez le planning des disponibilités de location de matériel wingfoil à {city_name}. Réservez votre créneau pour profiter du wingfoil dans les meilleures conditions."
    )
    return render_template('sites/planning.html', meta_tags=meta_tags, site=site)

@bp.route('/site/<site_slug>/contact', methods=['GET', 'POST'])
def contact(site_slug=None):
    site = None
    if site_slug:
        site = Site.query.filter_by(slug=site_slug).first_or_404()
        city_name = site.city
    else:
        # Pour la route globale
        city_name = "notre réseau"
    
    meta_tags = generate_meta_tags(
        title=f"Contact - Wing4All {city_name}",
        description=f"Contactez-nous pour louer votre matériel de wingfoil à {city_name}. Moniteurs FFV diplômés, nous vous accompagnons dans votre progression."
    )
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash('Votre message a été envoyé avec succès!', 'success')
        
        if site:
            return redirect(url_for('main.contact', site_slug=site_slug))
        else:
            return redirect(url_for('main.contact_franchise'))
    
    # Passer le template approprié selon le contexte
    if site:
        return render_template('sites/contact.html', meta_tags=meta_tags, site=site)
    else:
        return render_template('franchise/contact.html', meta_tags=meta_tags)

@bp.route('/contact', methods=['GET', 'POST'])
def contact_franchise():
    # Implémentation spécifique pour la route globale sans site_slug
    meta_tags = generate_meta_tags(
        title="Contact - Wing4All",
        description="Contactez-nous pour en savoir plus sur notre réseau de location de matériel de wingfoil en France. Nous sommes à votre écoute pour répondre à toutes vos questions."
    )
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash('Votre message a été envoyé avec succès!', 'success')
        return redirect(url_for('main.contact_franchise'))
    
    return render_template('franchise/contact.html', meta_tags=meta_tags)

@bp.route('/cgv')
def cgv():
    meta_tags = generate_meta_tags(
        title="Conditions Générales de Vente",
        description="Consultez les conditions générales de vente pour la location de matériel de wingfoil chez Wing4All."
    )
    return render_template('franchise/cgv.html', meta_tags=meta_tags)

@bp.route('/guide-debutant')
def beginner_guide():
    meta_tags = generate_meta_tags(
        title="Guide du Débutant en Wingfoil",
        description="Guide étape par étape pour apprendre le wingfoil : sécurité, théorie du vent, maniement de l'aile, premiers bords, empennage, vol et jibe."
    )
    return render_template('franchise/beginner_guide.html', meta_tags=meta_tags)

@bp.route('/articles-conseils/<article_name>')
def article_conseils(article_name):
    # Récupérer l'article par son slug
    article = get_article_by_slug(article_name)
    
    if not article:
        # Si l'article n'existe pas, rediriger vers la page d'actualités
        flash("L'article demandé n'existe pas.", "warning")
        return redirect(url_for('main.actualites'))
    
    # Utiliser les métadonnées de l'article pour la SEO
    meta_tags = generate_meta_tags(title=article.title, description=article.description)
    
    try:
        # Essayer de rendre le template approprié avec le template parent franchise
        return render_template(f'articles_conseils/{article_name}.html', 
                              meta_tags=meta_tags, 
                              article=article)
    except:
        # Si le template n'existe pas, rediriger vers la page d'actualités
        flash("L'article demandé n'existe pas.", "warning")
        return redirect(url_for('main.actualites'))

# Routes API pour le calendrier

@bp.route('/api/events', methods=['GET'])
def get_events():
    # Récupération des paramètres de requête
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    
    # Conversion des dates
    if start:
        start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
    else:
        start_date = datetime.now()
    
    if end:
        end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
    else:
        # Par défaut, on prend 3 mois
        end_date = start_date + timedelta(days=90)
    
    # Récupération des événements
    events = CalendarEvent.query.filter(
        CalendarEvent.end_time >= start_date,
        CalendarEvent.start_time <= end_date
    ).all()
    
    # Formatage des événements pour FullCalendar
    formatted_events = []
    for event in events:
        formatted_events.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
            'description': event.description,
            'is_available': event.is_available,
            'event_type': event.event_type,
            'backgroundColor': '#28a745' if event.is_available else '#ffc107' if event.event_type == 'busy' else '#dc3545'
        })
    
    return jsonify(formatted_events)

@bp.route('/api/events', methods=['POST'])
@login_required
def create_event():
    # Vérifier si l'utilisateur est un admin
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Permission refusée'}), 403
    
    data = request.json
    
    try:
        # Création de l'événement
        event = CalendarEvent(
            title=data.get('title'),
            start_time=datetime.fromisoformat(data.get('start_time')),
            end_time=datetime.fromisoformat(data.get('end_time')),
            description=data.get('description', ''),
            event_type=data.get('event_type', 'reservation'),
            is_available=data.get('is_available', True),
            created_by_id=current_user.id
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({'success': True, 'id': event.id})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/api/events/<int:event_id>', methods=['DELETE'])
@login_required
def delete_event(event_id):
    # Vérifier si l'utilisateur est un admin
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Permission refusée'}), 403
    
    try:
        event = CalendarEvent.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/api/bookings', methods=['POST'])
@login_required
def create_booking():
    data = request.json
    event_id = data.get('event_id')
    notes = data.get('notes', '')
    
    # Journalisation de débogage
    print(f"DEBUG - Tentative de réservation - Utilisateur: {current_user.id}, Événement: {event_id}")
    
    try:
        # Récupération de l'événement
        event = CalendarEvent.query.get_or_404(event_id)
        print(f"DEBUG - Événement trouvé: {event.title}, disponible: {event.is_available}")
        
        # Vérification que le créneau est bien disponible
        if not event.is_available:
            print(f"DEBUG - Créneau non disponible")
            return jsonify({'success': False, 'message': 'Ce créneau n\'est plus disponible'}), 400
        
        # Import du modèle de réservation
        from app.models.reservation import Reservation
        
        try:
            # Création d'une réservation
            reservation = Reservation(
                user_id=current_user.id,
                equipment_id=None,  # Maintenant nullable
                start_date=event.start_time,
                end_date=event.end_time,
                status='pending',
                notes=notes
            )
            
            db.session.add(reservation)
            db.session.commit()
            print(f"DEBUG - Réservation créée avec succès, ID: {reservation.id}")
            
            # Mise à jour de l'événement
            event.is_available = False
            event.reservation_id = reservation.id
            db.session.commit()
            print(f"DEBUG - Événement mis à jour")
            
            return jsonify({'success': True, 'id': reservation.id})
            
        except Exception as e:
            print(f"DEBUG - Erreur lors de la création de la réservation: {str(e)}")
            db.session.rollback()
            return jsonify({'success': False, 'message': f"Erreur lors de la création de la réservation: {str(e)}"}), 500
        
    except Exception as e:
        print(f"DEBUG - Erreur générale: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/partenariats')
def partenariats():
    meta_tags = generate_meta_tags(
        title="Nos partenariats - Wing4All",
        description="Découvrez les partenariats de Wing4All pour la promotion d'une pratique éco-responsable et accessible du wingfoil."
    )
    return render_template('franchise/partenariats.html', meta_tags=meta_tags)

@bp.route('/rejoindre')
def rejoindre():
    meta_tags = generate_meta_tags(
        title="Rejoindre le réseau Wing4All - Devenir franchisé",
        description="Découvrez comment rejoindre le réseau Wing4All et ouvrir votre propre franchise de location de wingfoil. Accompagnement complet et matériel fourni pour un démarrage réussi."
    )
    structured_data = generate_structured_data("Organization", {})
    return render_template('franchise/rejoindre.html', 
                          meta_tags=meta_tags,
                          structured_data=structured_data)

@bp.route('/rejoindre/etapes')
def rejoindre_etapes():
    meta_tags = generate_meta_tags(
        title="Les étapes pour rejoindre Wing4All - Processus détaillé",
        description="Le parcours détaillé pour rejoindre le réseau Wing4All : formulation du projet, étude de marché, budget, aspects juridiques, formation et lancement."
    )
    structured_data = generate_structured_data("Organization", {})
    return render_template('franchise/rejoindre/etapes.html', 
                          meta_tags=meta_tags,
                          structured_data=structured_data)