from app.auth import bp
from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash

@bp.route('/login')
def login():
    return render_template('auth/login.html')

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