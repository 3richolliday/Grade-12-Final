from flask_login import LoginManager
from app.models.user import User

login_manager = LoginManager()

login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(uiid):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(uiid)
