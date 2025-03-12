from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import create_app, db
from .models import User, Equipment, Reservation

app = create_app()

@app.route('/')
def home():
    equipment = Equipment.query.all()
    return render_template('equipment/index.html', equipment=equipment)

@app.route('/equipment/<int:id>')
def equipment_detail(id):
    equipment = Equipment.query.get_or_404(id)
    return render_template('equipment/equipment_detail.html', equipment=equipment)

@app.route('/reservation/<int:equipment_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('my_reservations'))
    return render_template('reservations/make_reservation.html', equipment=equipment)

@app.route('/my-reservations')
@login_required
def my_reservations():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('reservations/my_reservations.html', reservations=reservations)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Identifiants incorrects', 'danger')
            return redirect(url_for('login'))
        
        login_user(user)
        flash('Connexion réussie!', 'success')
        return redirect(url_for('home'))
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email déjà utilisé', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method='sha256')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Inscription réussie! Vous pouvez maintenant vous connecter', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True) 