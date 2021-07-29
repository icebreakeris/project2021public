"""
Starting point of the web app. 
Creates a new flask instance, runs it and then includes the views and api python files.

"""
from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, CSRFError

from sqlalchemy.exc import OperationalError

from json import JSONDecodeError

import os
import config

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig") #select the development config for now

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app) 
login_manager.login_view = "general.login"

csrf = CSRFProtect()
csrf.init_app(app)

db = SQLAlchemy(app)
db.init_app(app)

from .models import User

if not os.path.exists("app/"+config.DevelopmentConfig.DB_NAME): 
    app.logger.warn("No database was found. Created one.")
    db.create_all()

from app.views import admin, general, news, profile, search, lessons
app.register_blueprint(admin.mod)
app.register_blueprint(general.mod)
app.register_blueprint(news.mod)
app.register_blueprint(profile.mod)
app.register_blueprint(search.mod)
app.register_blueprint(lessons.mod)

@app.errorhandler(500)
@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(CSRFError)
@app.errorhandler(JSONDecodeError)
def website_error(error): 
    return render_template("pages/error.html", error=error)

@app.errorhandler(OperationalError)
def operational_error(error): 
    return render_template("pages/error.html", error=f"Internal Database Error. Please try again later.\n{error}")