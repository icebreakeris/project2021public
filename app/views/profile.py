from flask import(
    Blueprint, 
    render_template,
    url_for,
    redirect,
    flash, 
    abort, 
    jsonify, 
    request, 
    session
)
from flask_login import current_user, login_required

from app import db, csrf
from app.models import User, Article, Lesson

from app.forms import (
    ChangeEmailForm, 
    ChangePasswordForm, 
    ChangeUsernameForm, 
    NewsCheckboxForm,
    DeleteAccountForm
)


from app.util import Validators, Populators

import json

mod = Blueprint("profile", __name__, url_prefix="/profile")

@mod.route("/debug/populate_articles", methods=["GET", "POST"])
@login_required
@csrf.exempt
def populate_articles():
    Populators.populate_articles(db, count=10)
    return redirect(url_for("profile.profile"))

@mod.route("/debug/populate_lessons", methods=["GET", "POST"])
@login_required
@csrf.exempt
def populate_lessons():
    Populators.populate_lessons(db, count=10)
    return redirect(url_for("profile.profile"))

@mod.route("/", methods=("GET", "POST"))
@login_required
def profile():
    #the url parameter needs to be validated to avoid injections and stuff
    change_email_form = ChangeEmailForm()
    change_password_form = ChangePasswordForm()
    change_username_form = ChangeUsernameForm()
    news_checkbox_form = NewsCheckboxForm()
    delete_account_form = DeleteAccountForm()

    #populates checkbox choices by querying the database and getting all unique lesson topics
    topics = []
    for value in Lesson.query.distinct(Lesson.topic):
        if value.topic not in topics:
            topics.append(value.topic)

    news_checkbox_form.checkboxes.choices = [(i, i) for i in topics] #sets the topics to 

    user = User.query.filter_by(username=current_user.username).first()
    if user:
        confirmation_string = "DELETE_THIS_ACCOUNT"

        if request.method == "POST":
            if delete_account_form.confirmation_field.data and delete_account_form.validate_on_submit():
                if delete_account_form.confirmation_field.data == confirmation_string:
                    User.query.filter_by(id=current_user.id).delete()
                    db.session.commit()
                    flash("Your account has been deleted!")
                else: 
                    flash("Confirmation value wrong! Account not deleted.")
                return redirect(url_for("general.index"))
                
            #if a username change form has been submitted
            if change_username_form.username.data and change_username_form.validate_on_submit():
                username = change_username_form.username.data
                #validate the username first to ensure it does not contain any invalid characters,
                #and is not too long or too short
                if not Validators.validate_username(username):
                    flash("The username is invalid! Please try again using a different username.")
                    return redirect(url_for("profile.profile"))

                #then make sure that its not in the database
                if not bool(User.query.filter_by(username=username).first()):
                    user.username = username
                    db.session.commit()
                else:
                    flash("Username already used! Please use a different username.")
                    return redirect(url_for("profile.profile"))

                flash("Your username has been changed!")
                return redirect(url_for("profile.profile"))

            #if a change email form has been submitted
            if change_email_form.email.data and change_email_form.validate_on_submit():
                email = change_email_form.email.data

                #make sure the email is not already used
                if not (User.query.filter_by(email=email).first()):
                    #set that email for the user and commit to database
                    user.email = email
                    db.session.commit()
                else:
                    flash("Email is already used! Please use a different one.")
                    return redirect(url_for("profile.profile"))

                flash("Your email has been updated!")
                return redirect(url_for("profile.profile"))

            #if a password change form has been submitted
            if change_password_form.password.data and change_password_form.validate_on_submit():
                current_password = change_password_form.current_password.data
                password = change_password_form.password.data

                #checks the given password against a regex to find out whether it matches the requirements
                if not current_user.check_password(current_password):
                    flash("Incorrect password! No changes processed.")
                    return redirect(url_for("profile.profile"))
                
                if not Validators.validate_password(password):
                    flash("The new password did not meet the requirements!")
                    return redirect(url_for("profile.profile"))

                #commit to database
                user.update_password(password)
                db.session.commit()

                flash("Password has been updated!")
                return redirect(url_for("profile.profile"))
                
            #if a topic preference has been submitted
            if news_checkbox_form.validate_on_submit():
                #get the checked boxes from the form
                checkboxes = news_checkbox_form.checkboxes.data

                #set user preference column as the result
                user.preferences = json.dumps(checkboxes)
                db.session.commit()
                
                flash("Your lesson preferences have been updated!")
                return redirect(url_for("profile.profile"))

        preferences = json.loads(user.preferences)

        return render_template(
            "pages/profile.html",
            email_form=change_email_form,
            password_form=change_password_form,
            username_form=change_username_form,
            news_checkbox=news_checkbox_form,
            preferences=preferences,
            article_count=Article.query.count(),
            lesson_count=Lesson.query.count(),
            complete_lessons=get_complete_lessons(),
            delete_account_form=delete_account_form,
            confirmation_string=confirmation_string,
            badges = json.loads(current_user.badges_earned)
        )

    #not sure how a user would get here without being kicked out for not being logged in, but if they do
    #then throw a 500 error because the server must've failed somewhere
    return abort(500)

def get_complete_lessons(): 
    complete_lessons = {}
    if session["progress"]:
        for item in session["progress"]["lessons"]: 
            if session["progress"]["lessons"][item]["complete"]:
                    complete_lessons.update({item:session["progress"]["lessons"][item]})
    return complete_lessons