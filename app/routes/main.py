from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .seo import generate_meta_tags, generate_structured_data
from flask_login import current_user, login_required
from app.models.calendar import CalendarEvent
from app.models.article import get_sorted_articles, get_article_by_slug
from app import db
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    meta_tags = generate_meta_tags(
        title="Location de Wingfoil à Saint-Malo",
        description="Location de matériel de wingfoil à Saint-Malo. Wings, foils et planches de qualité pour tous les niveaux. Conseils et accompagnement personnalisé."
    )
    structured_data = generate_structured_data("LocalBusiness", {})
    return render_template('home.html', meta_tags=meta_tags, structured_data=structured_data)

@bp.route('/conseils')
def conseils():
    meta_tags = generate_meta_tags(
        title="Conseils Wingfoil",
        description="Conseils et astuces pour la pratique du wingfoil à Saint-Malo. Apprenez avec un moniteur FFV diplômé qui optimise votre courbe d'apprentissage."
    )
    return render_template('conseils.html', meta_tags=meta_tags)

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    meta_tags = generate_meta_tags(
        title="Contact - Wing4All",
        description="Contactez-moi pour louer votre matériel de wingfoil à Saint-Malo. Moniteur FFV diplômé, je vous accompagne dans votre progression."
    )
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash('Votre message a été envoyé avec succès!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', meta_tags=meta_tags)

@bp.route('/formules')
def formules():
    meta_tags = generate_meta_tags(
        title="Formules Location Wingfoil",
        description="Découvrez nos formules de location de matériel wingfoil à Saint-Malo. Prix attractifs et matériel de qualité pour tous les niveaux."
    )
    return render_template('formules.html', meta_tags=meta_tags)

@bp.route('/cgv')
def cgv():
    meta_tags = generate_meta_tags(
        title="Conditions Générales de Vente",
        description="Consultez les conditions générales de vente pour la location de matériel de wingfoil chez Wing4All."
    )
    return render_template('cgv.html', meta_tags=meta_tags)

@bp.route('/guide-debutant')
def beginner_guide():
    meta_tags = generate_meta_tags(
        title="Guide du Débutant en Wingfoil",
        description="Guide étape par étape pour apprendre le wingfoil : sécurité, théorie du vent, maniement de l'aile, premiers bords, empennage, vol et jibe."
    )
    return render_template('beginner_guide.html', meta_tags=meta_tags)

@bp.route('/actualites')
def actualites():
    meta_tags = generate_meta_tags(
        title="Actualités Wing4All",
        description="Suivez toutes les actualités de Wing4All : événements, nouveautés, promotions et informations sur la location de matériel de wingfoil."
    )
    # Récupérer les articles triés du plus récent au plus ancien
    articles = get_sorted_articles(reverse=True)
    return render_template('actualites.html', meta_tags=meta_tags, articles=articles)

@bp.route('/planning')
def planning():
    meta_tags = generate_meta_tags(
        title="Planning et Disponibilités",
        description="Consultez le planning des disponibilités de location de matériel wingfoil. Réservez votre créneau pour profiter du wingfoil dans les meilleures conditions."
    )
    return render_template('planning.html', meta_tags=meta_tags)

@bp.route('/events')
def events():
    meta_tags = generate_meta_tags(
        title="Événements Wingfoil - Wing4All",
        description="Découvrez les événements wingfoil organisés à Saint-Malo. Initiations, compétitions et rencontres autour de la pratique du wingfoil."
    )
    # Récupérer les prochains événements
    now = datetime.now()
    upcoming_events = CalendarEvent.query.filter(
        CalendarEvent.start_time >= now,
        CalendarEvent.event_type == 'event'
    ).order_by(CalendarEvent.start_time).limit(10).all()
    
    return render_template('events.html', meta_tags=meta_tags, events=upcoming_events)

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
        # Essayer de rendre le template approprié
        return render_template(f'articles_conseils/{article_name}.html', meta_tags=meta_tags, article=article)
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