from app.assess import bp
from flask import render_template, session, redirect, url_for
from flask_login import login_required, current_user

from app.models.item import Item
from app.models.user_assessment import User_Assessment
from app.models.user_assessment_detail import User_Assessment_Detail
from app.sqla import sqla
from sqlalchemy import and_

SESSION_VAR_ASSESSMENT_ID = 'assessment_id'
SESSION_VAR_ASSESSMENT_DETAIL_ID = 'assessment_detail_id'

@bp.route('/select_language')
@login_required
def select_language():
    return render_template('assess/select_language.html', name=current_user.name)

@bp.route('/present_question')
@login_required
def present_question():
    
    # TBD: Instance the assessment here
    assessment = User_Assessment.query.filter(User_Assessment.user_id == current_user.id).first()
    session[SESSION_VAR_ASSESSMENT_ID] = assessment.id

    detail_for_next_question = get_next_assessment_detail(assessment);
    
    if detail_for_next_question:
        question = detail_for_next_question.item.question   
        session[SESSION_VAR_ASSESSMENT_DETAIL_ID] = detail_for_next_question.id
        return render_template('assess/present_question.html', question=question)
    else:
        return redirect(url_for("assess.assessment_complete"))

@bp.route('/present_question', methods=['POST'])
@login_required
def present_question_post():
    
    assessment_id = session[SESSION_VAR_ASSESSMENT_ID]
    assessment = User_Assessment.query.filter(User_Assessment.id == assessment_id)

    assessment_detail_id = session[SESSION_VAR_ASSESSMENT_DETAIL_ID]
    detail = User_Assessment_Detail.query.filter(User_Assessment_Detail.id == assessment_detail_id).first()

    detail.score = 0.5
    sqla.session.commit()

    return redirect(url_for("assess.present_question"))

@bp.route('/assessment_complete')
@login_required
def assessment_complete():
    return render_template('assess/assessment_complete.html')


def get_next_assessment_detail(assessment):
    
    detail = User_Assessment_Detail.query.filter(
        (User_Assessment_Detail.user_assessment_id == assessment.id) & 
        (User_Assessment_Detail.score == None)).first()
    
    return detail