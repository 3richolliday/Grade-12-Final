from datetime import date, datetime
from app.assess import bp
from flask import render_template, session, redirect, url_for
from flask_login import login_required, current_user
from app.assess.enums import Language_Type

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

@bp.route('/select_language', methods=['POST'])
@login_required
def select_language_post():

    assessment = User_Assessment(user_id=current_user.id)

    sqla.session.add(assessment)
    sqla.session.commit()
    
    items = Item.query.filter(Item.language == Language_Type.EN)
    
    user_assessment_details = []

    for item in items:
        user_assessment_detail = User_Assessment_Detail(user_assessment_id=assessment.id, item_id=item.id)
        user_assessment_details.append(user_assessment_detail)

    sqla.session.add(assessment)
    sqla.session.add_all(user_assessment_details)
    sqla.session.commit()

    return redirect(url_for("assess.present_question"))


@bp.route('/present_question')
@login_required
def present_question():
    
    # Get the next assessment for this user which isn't complete
    assessment = User_Assessment.query.filter((User_Assessment.user_id == current_user.id) &
        (User_Assessment.date_completed == None)).first()
    session[SESSION_VAR_ASSESSMENT_ID] = assessment.id

    detail_for_next_question = get_next_assessment_detail(assessment);
    
    if detail_for_next_question:
        question = detail_for_next_question.item.question   
        session[SESSION_VAR_ASSESSMENT_DETAIL_ID] = detail_for_next_question.id
        return render_template('assess/present_question.html', question=question)
    else:
        score_assessment(assessment);
        return render_template('assess/assessment_complete.html', assessment=assessment)

@bp.route('/present_question', methods=['POST'])
@login_required
def present_question_post():
    
    assessment_id = session[SESSION_VAR_ASSESSMENT_ID]
    assessment = User_Assessment.query.filter(User_Assessment.id == assessment_id)

    assessment_detail_id = session[SESSION_VAR_ASSESSMENT_DETAIL_ID]
    detail = User_Assessment_Detail.query.filter(User_Assessment_Detail.id == assessment_detail_id).first()

    detail.score = detail.item.weight
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

def score_assessment(assessment):
    details = User_Assessment_Detail.query.filter(
        (User_Assessment_Detail.user_assessment_id == assessment.id) & 
        (User_Assessment_Detail.score != None))
    
    total_score_possible = 0
    total_score = 0

    for detail in details:
        total_score_possible += detail.item.weight
        total_score += detail.score
        
    assessment.total_score_possible = total_score_possible
    assessment.total_score = total_score
    assessment.date_completed = date.today()

    sqla.session.commit()