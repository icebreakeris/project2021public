from flask import Blueprint, render_template, redirect, flash, request, abort
from flask_login import login_required, current_user

from app import db
from app.models import Lesson, User
from app.util import Populators, Utilities

import json

mod = Blueprint("lessons", __name__, url_prefix="/lessons")

@mod.route("/")
def lessons():
    #Gets the most recently featured lesson
    #in case there are more than one featured lesson
    featured_lesson = Lesson.query.filter_by(featured=1).order_by(Lesson.id.desc()).first()

    #if the user is logged in
    if current_user.is_authenticated:
        #get their preferences 
        preferences = json.loads(current_user.preferences)

        if preferences: 
            #get all preferred lessons
            preferred_lessons = Lesson.query.filter(Lesson.topic.in_((preferences))).order_by(Lesson.id.desc()).all()
            if preferred_lessons:
                #get lessons that are not preferred by the user
                other_lessons = Lesson.query.filter(Lesson.topic.notin_((preferences))).order_by(Lesson.id.desc()).all()
                return render_template(
                    "pages/lessons.html",
                    preferred_lessons=preferred_lessons,
                    lessons=other_lessons,
                    featured_lesson=featured_lesson,
                    preferences=preferences
                )
    
    #if the user is not logged in, then get all lessons
    lessons = Lesson.query.order_by(Lesson.id.desc()).all()

    return render_template(
        "pages/lessons.html",
        lessons = lessons,
        featured_lesson=featured_lesson
    )
    

@mod.route("/<int:lesson_id>", methods=["POST", "GET"])
#@login_required
def lesson(lesson_id):
    questions = None
    badges = None

    lesson = Lesson.query.filter_by(id=lesson_id).first()

    if not lesson: 
        return abort(404)

    next_lesson = Lesson.query.filter_by(topic=lesson.topic).filter(Lesson.id > lesson.id ).first()
    lesson_json = json.loads(lesson.content)
    print(lesson_json)
    #if the user is logged in
    if current_user.is_authenticated:

        #if the lesson contains questions
        if lesson.questions:
            questions = json.loads(lesson.questions)
            #print(json.dumps(questions, indent=4))
            if request.method == "POST" and request.form:
                results = {}
                total_correct = 0
                for key, value in request.form.items():
                    correct = questions[key]["answers"][value]["answer"]
                    if correct:
                        total_correct += 1

                    results.update({key:correct})
                    register_question_attempt(lesson, total_correct)
                return json.dumps(results)

        register_question_attempt(lesson)


        badges = json.loads(current_user.badges_earned)

    return render_template(
        "pages/lesson.html",
        lesson=lesson,
        content=lesson_json,
        questions=questions,
        badge=lesson.badge,
        badge_url=lesson.badge_url,
        next_lesson=next_lesson,
        badges = badges
    )

def register_question_attempt(lesson, total_correct=0):
    progress = json.loads(current_user.progress)
    badges = json.loads(current_user.badges_earned)
    
    try: 
        #json.loads can fail and throw an exception if it tries deserializing an item of type none
        amount_of_questions = len(json.loads(lesson.questions))
    except:
        amount_of_questions=0

    #if the lesson is not recorded in the user's progress dictionary
    if str(lesson.id) not in progress["lessons"]:
        complete = False

        #if there are no questions in the lesson then mark it as complete
        if amount_of_questions <= 0:
            complete=True

        #if there are then mark it as incomplete and set the total
        progress["lessons"].update({str(lesson.id):{
            "title":lesson.title,
            "complete":complete,
            "lessons_correct":total_correct,
            "total_questions": amount_of_questions
        }})
        
        current_user.progress = json.dumps(progress)
        db.session.commit()

    #if lesson does not have any questions and for some reason is not marked as complete
    #ensure it is marked 
    if amount_of_questions <= 0 and not progress["lessons"][str(lesson.id)]["complete"]:
        progress["lessons"].update({str(lesson.id):{
            "title":lesson.title,
            "complete":True,
            "lessons_correct":0,
            "total_questions": 0
        }})
        
    #if all questions are correct
    if amount_of_questions == total_correct:
        progress["lessons"].update({str(lesson.id):{
            "title":lesson.title,
            "complete":True,
            "lessons_correct":total_correct,
            "total_questions":amount_of_questions
        }})

        if lesson.badge:
            register_badge_award(lesson)
    
    #if not 
    elif total_correct != 0: 
        progress["lessons"].update({str(lesson.id):{
            "title":lesson.title,
            "complete":False,
            "lessons_correct":total_correct,
            "total_questions":amount_of_questions
        }})
    
    current_user.progress = json.dumps(progress)
    db.session.commit()

def register_badge_award(lesson): 
    badges = json.loads(current_user.badges_earned)

    #if the badge is already earned
    if str(lesson.id) in badges: 
        return

    badges.update({str(lesson.id):{
        "badge_name":lesson.badge,
        "badge_url":lesson.badge_url
    }})

    current_user.badges_earned = json.dumps(badges)
    db.session.commit()
