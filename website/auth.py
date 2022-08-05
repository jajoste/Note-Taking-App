from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from website import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint('auth', __name__,)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user=user, remember=True)
                flash('Logged in, successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Account does not exist', category="error")

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method=='POST':
        email = request.form.get('email').lower()
        fName = request.form.get('fName').title()
        lName = request.form.get('lName').title()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account already exists', category='error')
        elif len(email) < 1:
            flash('Please enter an email address', category='error')
        elif len(fName) < 1:
            flash('Please enter a First Name',category="error")
        elif len(lName) < 1:
            flash('Please enter a Last Name', category='error')
        elif len(password1) < 7:
            flash('Password must contain 7 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            new_user = User(email=email, first_name=fName, last_name=lName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user, remember=True)
            flash('Account created!',category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
