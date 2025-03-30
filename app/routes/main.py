from flask import Blueprint, render_template, request, flash, redirect, url_for
from .seo import generate_meta_tags, generate_structured_data

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