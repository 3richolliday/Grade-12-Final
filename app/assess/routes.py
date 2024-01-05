from app.assess import bp
from flask import render_template
from flask_login import login_required, current_user

@bp.route('/select_language')
@login_required
def select_language():
    return render_template('assess/select_language.html', name=current_user.name)