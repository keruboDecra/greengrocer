from . import auth
from flask import render_template, request, flash, redirect, url_for
from ..models import User, Product
from flask_login import login_user, logout_user, current_user, login_required
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not user.verify_password(password):
            flash('Incorrect email or password')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash('Successfully in')
        return redirect(request.args.get('next') or url_for('main.products'))
    
    if current_user.is_authenticated:
        flash('Aready in')
        return redirect(request.args.get('next') or url_for('main.products'))
        
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        location = request.form.get('location')
        country = request.form.get('country')
        role = 'Client'

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already in use')
            return redirect(url_for('auth.register'))

        new_user = User(name=name, email=email, location=location, country=country, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/register_business', methods=['GET', 'POST'])
def register_business():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        location = request.form.get('location')
        country = request.form.get('country')
        seller = request.form.get('seller')
        role = 'Seller'
        if seller == "company":
            name += '|' + request.form.get('co_number')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Business email already in use')
            return redirect(url_for('auth.register_business'))
        
        new_user = User(name=name, email=email, location=location, country=country, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register_business.html')

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))