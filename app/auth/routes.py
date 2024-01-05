from app.auth import bp

@bp.route('/login')
def login():
    return 'Login'

@bp.route('/signup')
def signup():
    # Create test user
    # from app.models.user import User
    # from app.sqla import sqla
    # user = User(id=2, email="ericholliday20@gmail.com", username="eholliday")
    # sqla.session.add(user)
    # sqla.session.commit()
    return 'Signup'

@bp.route('/logout')
def logout():
    return 'Logout'