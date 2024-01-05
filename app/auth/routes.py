from app.auth import bp
from flask import render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from flask_login import login_user, login_required, logout_user
from app.sqla import sqla

@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/login', methods=['POST'])
def login_post():
    
    email = request.form.get('email').lower()
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 
    
    # Have flask-login start to manage our session
    login_user(user, remember=remember)

    return redirect(url_for('assess.select_language'))

@bp.route('/signup')
def signup():
    # Create test user
    # from app.models.user import User
    # from app.sqla import sqla
    # user = User(id=1, email="ericholliday20@gmail.com", name="eholliday", 
    #             password=generate_password_hash("abc"))
    # sqla.session.add(user)
    # sqla.session.commit()
    return render_template('auth/signup.html')

@bp.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email').lower()
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password))

    # add the new user to the database
    sqla.session.add(new_user)
    sqla.session.commit()

    return redirect(url_for('auth.login'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))