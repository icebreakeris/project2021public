#pylint: disable=no-member

from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from flask_login import login_required, login_user, logout_user, current_user

from app import db, bcrypt, login_manager, app
from app.forms import LoginForm, RegisterForm
from app.models import User, Article, Lesson
from app.util import Validators

from datetime import datetime

import json


mod = Blueprint("general", __name__)

#checks if the password has at least one lowercase letter, one upper case letter,
#at least one number, a special character and is at least 7 characters long

@mod.route("/")
def index():
    placeholder_lesson = Lesson(
        author="Author",
        title="Learn to create strong passwords!",
        summary="This lesson will focus on explaining why strong passwords are important and will teach you how to make one!",
        featured = False,
        topic="Passwords"
    )
    #get 5 newest articles from the database

    articles = Article.query.order_by(Article.date_posted.desc()).limit(5).all()
    lessons = Lesson.query.order_by(Lesson.date_created.desc()).limit(5).all()

    if articles:
        current_date = datetime.now()

        for i, j in enumerate(articles):
            days_old = (current_date-j.date_posted).days
            if days_old < 5: #checks if the article is older than 5 days
                #if it isn't then it adds a [New] badge
                articles[i].title = j.title + "<span class='badge badge-secondary ml-2'>New</span>"

    return render_template(
        "pages/index.html",
        articles=articles,
        lessons=lessons,
        placeholder_lesson = placeholder_lesson
    )

@mod.route("/login", methods=("GET", "POST"))
def login():
    #Check if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for("general.index"))

    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            #get user data from the database
            user = User.query.filter_by(username=form.username.data).first()
            #check if the data is valid and the password is correct
            if user and user.check_password(form.password.data):
                if not user.active:
                    app.logger.info(f"User tried to log in with a deactivated account. [username:{user.username} - email:{user.email}]")
                    flash("This account has been deactivated. Contact website administration.")
                    return redirect(url_for("general.login")) 

                user.last_login = datetime.now() 
                db.session.commit()
                login_user(user)
                app.logger.info(f"Successful login. [username:{user.username} - email:{user.email}]")
                return redirect(url_for("general.index"))
            else:
                app.logger.info(f"Invalid login attempt. [username:{form.username.data}]")
                flash("Invalid username or password!")
        else: 
            app.logger.info(f"Invalid login attempt with bad data. [form:{form}]")
            flash("Invalid username or password!")
            
    return render_template(
        "pages/login.html", 
        form=form
    )

@mod.route("/register", methods=("GET", "POST"))
def register():
    #if the user is logged in, prevent them from registering 
    if current_user.is_authenticated: 
        return redirect(url_for("general.index"))

    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            #if the username is less than 3 characters 
            if not Validators.validate_username(form.username.data): 
                flash("Chosen username is invalid! Please choose another one and try again.")
                return redirect(url_for("general.register"))

            #if the database does not contain an account with the same username
            if not bool(User.query.filter_by(username=form.username.data).first()):
                #if the database does not contain an account with the same email
                if not bool(User.query.filter_by(email=form.email.data).first()):
                    #validate the password
                    if not Validators.validate_password(form.password.data):
                        flash("Password did not match the requirements!")
                        return redirect(url_for("general.register"))

                    #creates a user object 
                    user = User(
                        username=form.username.data,
                        email=form.email.data,
                        password=form.password.data
                    )

                    #adds the user to the database
                    db.session.add(user)
                    #stores data 
                    db.session.commit()
                    flash("Successfully registered! You can log in now.")
                    app.logger.info(f"A user has registered! [username:{form.username.data} - email:{form.email.data}]")
                else:
                    flash("Email already used!")
                    app.logger.info(f"Someone tried to use an already in use email. [username:{form.username.data} - email:{form.email.data}]")
                    return redirect(url_for("general.register"))
            else:
                flash("Username already used!")
                app.logger.info(f"Someone tried to use an already in use username. [username:{form.username.data} - email:{form.email.data}")
                return redirect(url_for("general.register"))
            return redirect(url_for("general.login"))
        else:
            app.logger.info(f"Someone provided invalid form data in register. {form.data}")
            flash("Invalid details!")
 
    return render_template(
        "pages/register.html", 
        form=form
    )

    
@mod.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("general.index"))

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter(User.id==user_id).first()

    #in case the user's account gets deactivated while they are
    #logged in

    if user: 
        if not user.active: 
            app.logger.info(f"User's account got deactivated while they were logged on. [username:{user.username} - email:{user.email}]")
            session.clear()
            return None 
            
        session["progress"]=json.loads(user.progress)
    else: 
        #if for whatever reason the anonymous session contains progress dictionary, clear it
        if session["progress"]:
            app.logger.error("Anonymous session contained 'progress'. Clearing it...")
            session.clear()
    return user

#render article with its id
#get article data from the database
#use the data to render that page

