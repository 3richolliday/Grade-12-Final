from app.assess import bp
from flask import render_template
from flask_login import login_required, current_user

from app.models.item import Item
from app.models.user_assessment import User_Assessment
from app.models.user_assessment_detail import User_Assessment_Detail
from app.sqla import sqla
from sqlalchemy import and_

@bp.route('/select_language')
@login_required
def select_language():
    return render_template('assess/select_language.html', name=current_user.name)

@bp.route('/present_question')
@login_required
def present_question():
    assessment = User_Assessment.query.filter(User_Assessment.user_id == current_user.id).first()
    
    detail = User_Assessment_Detail.query.filter(
        (User_Assessment_Detail.user_assessment_id == assessment.id) & 
        (User_Assessment_Detail.score == None)).first()
    
    question = detail.item.question

    detail.score = 0.5
    sqla.session.commit()

    return render_template('assess/present_question.html', question=question)