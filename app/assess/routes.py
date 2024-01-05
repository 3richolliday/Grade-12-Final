from app.assess import bp
from flask import render_template

@bp.route('/select_language')
def select_language():
    return render_template('assess/select_language.html')