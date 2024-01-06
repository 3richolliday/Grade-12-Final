from app.assess import bp
from flask import render_template
from flask_login import login_required, current_user

from app.models.item import Item
from app.models.user_assessment import User_Assessment
from app.models.user_assessment_detail import User_Assessment_Detail

@bp.route('/select_language')
@login_required
def select_language():
    for assessment in User_Assessment.query.filter_by(user_id=current_user.id):
        detail = User_Assessment_Detail.query.filter_by(user_assessment_id=assessment.id).first()

    return render_template('assess/select_language.html', name=current_user.name)