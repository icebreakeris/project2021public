from flask import Blueprint, render_template, url_for, redirect, flash, abort, request

from app import db
from app.models import Article, Lesson
from app.forms import SearchForm

from sqlalchemy import or_

mod = Blueprint("search", __name__, url_prefix="/search")

@mod.route("/", methods=("GET", "POST"))
def search():
    form = SearchForm()

    if form.validate_on_submit():
        query = form.search.data

        #this gets all articles/lessons that contain the query in their topic or title columns
        #for example, a query of "malware" will return all articles/lessons with the topic of "malware"
        #and all articles/lessons that have "malware" in their titles
        articles = Article.query.filter(
            or_(
                Article.title.contains(query),
                Article.topic.contains(query)
            )
        ).order_by(Article.date_posted.desc()).all()

        lessons = Lesson.query.filter(
            or_(
                Lesson.title.contains(query),
                Lesson.topic.contains(query)
            )
        ).order_by(Lesson.date_created.desc()).all()

        return render_template("pages/search.html", articles=articles, lessons=lessons)

    return redirect(url_for("general.index"))