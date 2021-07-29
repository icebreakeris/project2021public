"""
Database models of the project.

"""

from app import db, bcrypt
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True) 
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    is_editor = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    registered = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime, nullable=True)
    preferences = db.Column(db.Text, nullable=False)
    progress = db.Column(db.Text, nullable=False)
    badges_earned = db.Column(db.Text, nullable=False)

    def __init__(self, username, email, password, badges_earned="{}", preferences="[]", progress="{\"lessons\":{}}", active=True, is_admin=False, is_editor=False): 
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        self.active = active 
        self.is_admin = is_admin
        self.is_editor = is_editor
        self.registered = datetime.now()
        self.preferences = preferences
        self.progress = progress
        self.badges_earned = badges_earned

    def check_password(self, plaintext): 
        return bcrypt.check_password_hash(self.password_hash, plaintext)

    def update_password(self, plaintext): 
        self.password_hash = bcrypt.generate_password_hash(plaintext).decode("utf-8")

class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), db.ForeignKey("users.username"))
    image_url = db.Column(db.Text, nullable=True)
    title = db.Column(db.String(120), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    last_edit = db.Column(db.DateTime, nullable=True)
    topic = db.Column(db.Text, nullable=False)

    def __init__(self, author, image_url, topic="", title="NO TITLE", summary="NO SUMMARY", content="NO CONTENT"):
        self.author = author
        self.image_url = image_url
        self.title = title 
        self.summary = summary
        self.content = content
        self.date_posted = datetime.now()
        self.topic = topic

class Lesson(db.Model): 
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Text, db.ForeignKey("users.username"))
    title = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    featured = db.Column(db.Boolean, nullable=False)
    topic = db.Column(db.Text, nullable=False)
    questions = db.Column(db.Text, nullable=True)
    badge = db.Column(db.Text, nullable=True)
    badge_url = db.Column(db.Text, nullable=True)

    def __init__(self, author, badge=None, badge_url=None, questions=None, title="NO TITLE", summary="NO SUMMARY", featured=False, topic="", content="NO CONTENT"):
        self.author = author
        self.title = title
        self.summary = summary
        self.date_created = datetime.now()
        self.featured = featured
        self.topic = topic
        self.content = content
        self.questions = questions
        self.badge = badge
        self.badge_url = badge_url
