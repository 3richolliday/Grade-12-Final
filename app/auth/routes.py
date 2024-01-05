from app.auth import bp
from flask import render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from flask_login import login_user

@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/login', methods=['POST'])
def login_post():
    
    email = request.form.get('email')
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
    # user = User(id=1, email="ericholliday20@gmail.com", username="eholliday", 
    #             password=generate_password_hash("abc"))
    # sqla.session.add(user)
    # sqla.session.commit()
    return 'Signup'

@bp.route('/logout')
def logout():
    return 'Logout'