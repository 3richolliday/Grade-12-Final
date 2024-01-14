from datetime import date, datetime
import logging
import random
from app.assess import bp
from flask import flash, render_template, session, redirect, url_for, request
from flask_login import login_required, current_user
from app.assess.enums import Item_Type, Language_Type

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

    try:
    
        language = request.form["language"]

        if language == 'EN':
            language = Language_Type.EN
        else:
            language = Language_Type.FR    
        
        assessment = User_Assessment(user_id=current_user.id)

        sqla.session.add(assessment)
        sqla.session.commit()
        
        # Get the list of items to be presented, and shuffle them
        items = Item.query.filter(Item.language == language)
        shuffled_items = items.all()
        random.shuffle(shuffled_items)
        
        user_assessment_details = []

        for item in shuffled_items:
            user_assessment_detail = User_Assessment_Detail(user_assessment_id=assessment.id, item_id=item.id)
            user_assessment_details.append(user_assessment_detail)

        sqla.session.add(assessment)
        sqla.session.add_all(user_assessment_details)
        sqla.session.commit()

        return redirect(url_for("assess.present_question"))
    except:
        logging.exception('')

    flash('Please select a language.')
    return redirect(url_for("assess.select_language"))

@bp.route('/present_question')
@login_required
def present_question():
    
    # Get the next assessment for this user which isn't complete
    assessment = User_Assessment.query.filter((User_Assessment.user_id == current_user.id) &
        (User_Assessment.date_completed == None)).first()
    session[SESSION_VAR_ASSESSMENT_ID] = assessment.id
    
    detail_for_next_question = get_next_assessment_detail(assessment);
    
    if detail_for_next_question:

        session[SESSION_VAR_ASSESSMENT_DETAIL_ID] = detail_for_next_question.id
        
        itemText = detail_for_next_question.item.question
        if detail_for_next_question.item.type == Item_Type.MC:
            return render_MC(detail_for_next_question)
        elif detail_for_next_question.item.type == Item_Type.FITB:
            return render_FITB(detail_for_next_question)
        # else:

    else:
        score_assessment(assessment);

        assessments = User_Assessment.query.filter(User_Assessment.user_id == current_user.id)
        return render_template('assess/assessment_complete.html', assessment=assessment, assessments=assessments)

def render_MC(detail_for_next_question):    
    itemText = detail_for_next_question.item.question
    
    parts = itemText.split('\\t')

    question = parts[0]
    distractorA = parts[1]
    distractorB = parts[2]
    distractorC = parts[3]
    distractorD = parts[4]

    return render_template('assess/present_mc.html', 
                        question=question,
                        distractorA=distractorA,
                        distractorB=distractorB,
                        distractorC=distractorC,
                        distractorD=distractorD)

def render_FITB(detail_for_next_question):
    itemText = detail_for_next_question.item.question

    return render_template('assess/present_fitb.html', 
                                question=itemText)

@bp.route('/present_mc', methods=['POST'])
@login_required
def present_mc():
    try:
        r = request.form["distractor"]
        return question_post_handler(r)
    except:
        logging.exception('')

    flash('Please select an answer.')
    return redirect(url_for("assess.present_question"))

@bp.route('/present_fitb', methods=['POST'])
@login_required
def present_fitb():
    try:
        r = request.form["answer"]
        return question_post_handler(r)
    except:
        logging.exception('')
    
    flash('Please select an answer.')
    return redirect(url_for("assess.present_question"))


def question_post_handler(r):
    
    assessment_id = session[SESSION_VAR_ASSESSMENT_ID]
    assessment = User_Assessment.query.filter(User_Assessment.id == assessment_id)

    assessment_detail_id = session[SESSION_VAR_ASSESSMENT_DETAIL_ID]
    detail = User_Assessment_Detail.query.filter(User_Assessment_Detail.id == assessment_detail_id).first()
    
    if r.lower() == detail.item.answer.lower():
        detail.score = detail.item.weight
    else:
        detail.score = 0

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