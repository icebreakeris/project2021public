from flask import Blueprint, render_template, url_for, flash, abort, redirect, session
from flask_login import current_user

from app import db
from app.models import Article, User, Lesson
from app.forms import SearchForm, TopicCheckboxForm
from app.util import Populators

from sqlalchemy import or_

import json 
from math import ceil

mod = Blueprint("news", __name__, url_prefix="/news")

#used to determine how many articles are shown in a single page, e.g. setting this
#to 10, will show 10 articles per page
PAGE_COUNT = 5   

@mod.route("/", defaults={"page_num" : 1}, methods=("GET", "POST"))
@mod.route("/<int:page_num>")
def news(page_num):
    articles = None
    count = 0

    if page_num <= 0:
        return redirect(url_for("news.news", page_num=1))

    topic_form = TopicCheckboxForm()
    
    topics = []
    for value in Article.query.distinct(Article.topic):
        if value.topic not in topics: 
            topics.append(value.topic)

    topic_form.checkboxes.choices = [(i,i) for i in topics]

    if topic_form.validate_on_submit():
        preferred_topics = topic_form.checkboxes.data 
        #here a session cookie is used to store the preferred topics that the user wishes to view
        #since a user does not need to be logged in to view the articles, saving these preferences
        #to a database is pointless, because the preferences would work for the logged in users and not
        #for logged out ones. This will work for both logged in users and logged out.
        session["preferred_topics"] = preferred_topics

        #redirect the user back to the news page to prevent "form resubmission" error when the user tries to go back
        #after viewing an article
        return redirect(url_for("news.news"))

    #if preferred topics session cookie is set, then get all articles based 
    #on the preferred topics
    if "preferred_topics" in session and len(session["preferred_topics"]) > 0:
        preferences = session["preferred_topics"]
        query = Article.query.filter(Article.topic.in_((preferences))).order_by(Article.date_posted.desc())
        articles = query.paginate(page_num, PAGE_COUNT, False).items
        count = query.count()
    else:
        #if there are no preferred articles then show everything
        query = Article.query.order_by(Article.date_posted.desc())
        articles = query.paginate(page_num, PAGE_COUNT, False).items
        count=query.count()
    
    #if there are no articles to show then render the page without any content
    if count <= 0:
        return render_template("pages/news.html")

    page_max = int(ceil(count/PAGE_COUNT))
    if page_num > page_max: 
        return redirect(url_for(
            "news.news", 
            page_num=page_max
        ))
    
    return render_template(
        "pages/news.html", 
        articles=articles, 
        page_num=page_num, 
        count=page_max,
        topic_form=topic_form
    )

@mod.route("/article/<int:article_id>")
def article(article_id):
    if article_id < 0: 
        return abort(404)

    #gets article based on its id
    article = Article.query.filter_by(id=article_id).first()
    if article:
        #if the article is valid, then get the json from the content_json column
        article_json = json.loads(article.content)

        #gets all articles based on the current article's topic
        similar_articles = Article.query.filter_by(topic=article.topic).filter(Article.id.isnot(article.id)).limit(5).all()
        related_lessons = Lesson.query.filter_by(topic=article.topic).limit(5).all()

        return render_template(
            "pages/article.html",
            article=article,
            article_json=article_json,
            similar_articles=similar_articles,
            related_lessons=related_lessons
        )

    else:
        #throw a 404 because the article wasn't found
        abort(404)