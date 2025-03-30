from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from .. import db
from .seo import generate_meta_tags

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    meta_tags = generate_meta_tags(
        title="Connexion",
        description="Connectez-vous à votre compte Wing4All pour gérer vos réservations de matériel wingfoil."
    )
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Identifiants incorrects', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        flash('Connexion réussie!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('auth/login.html', meta_tags=meta_tags)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    meta_tags = generate_meta_tags(
        title="Inscription",
        description="Créez votre compte Wing4All pour réserver votre matériel de wingfoil à Saint-Malo."
    )
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email déjà utilisé', 'danger')
            return redirect(url_for('auth.register'))
        
        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method='sha256')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Inscription réussie! Vous pouvez maintenant vous connecter', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', meta_tags=meta_tags)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('main.home')) 