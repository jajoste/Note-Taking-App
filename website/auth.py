from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__,)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return '<h1>Logout</h1>'

@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    if request.method=='POST':
        email = request.form.get('email')
        fName = request.form.get('fName')
        lName = request.form.get('lName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if len(email) < 1:
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
            flash('Account created!',category='success')

    return render_template("sign_up.html")
