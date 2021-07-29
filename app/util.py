import re
import json

import string
import random

from flask import url_for

from app import app
from app.models import Article, Lesson, User

class Validators(object): 
    password_regex = r"^((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9])(?=.\S*[!@#$&*]).{7,})\S$"
    username_regex = r"^[a-zA-Z0-9]*$"
    min_username_length = 3
    max_username_length = 30

    @classmethod
    def validate_password(cls, plaintext): 
        return bool(re.match(cls.password_regex, plaintext))

    @classmethod
    def validate_username(cls, username): 
        length = len(username)
        if length >= cls.min_username_length and length <= cls.max_username_length:
            if bool(re.match(cls.username_regex, username)):
                return True
        return False

class Populators():
    lesson_count = 10
    article_json = {"html":"\n                    <div class=\"article-paragraph\">\n                        <h3>Article heading 1</h3>\n                        <img src=\"/static/img/placeholder.png\" class=\"img-fluid float-right ml-4\" style=\"max-width:200px\">\n                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras magna mi, fermentum vel metus vel, varius accumsan diam. Morbi mattis, velit eget venenatis pulvinar, odio dui interdum eros, eget egestas justo mi sit amet lorem. Donec venenatis, felis et volutpat viverra, augue arcu dictum risus, vel mollis nibh sapien id diam. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec sagittis nibh. Aliquam quis magna quam. Maecenas accumsan, enim vel varius sodales, massa libero placerat neque, id elementum nunc massa nec tortor. Nam vehicula orci quis libero pellentesque vestibulum.</p>  \n                    </div>\n                    <div class=\"article-paragraph\">\n                        <h3>Article heading 2</h3>\n                        <img src=\"/static/img/placeholder.png\" class=\"img-fluid float-left mr-4\" style=\"max-width:200px\">\n                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras magna mi, fermentum vel metus vel, varius accumsan diam. Morbi mattis, velit eget venenatis pulvinar, odio dui interdum eros, eget egestas justo mi sit amet lorem. Donec venenatis, felis et volutpat viverra, augue arcu dictum risus, vel mollis nibh sapien id diam. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec sagittis nibh. Aliquam quis magna quam. Maecenas accumsan, enim vel varius sodales, massa libero placerat neque, id elementum nunc massa nec tortor. Nam vehicula orci quis libero pellentesque vestibulum.</p>  \n                    </div>\n                    <div class=\"article-paragraph\">\n                        <h3>Article heading 3</h3>\n                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras magna mi, fermentum vel metus vel, varius accumsan diam. Morbi mattis, velit eget venenatis pulvinar, odio dui interdum eros, eget egestas justo mi sit amet lorem. Donec venenatis, felis et volutpat viverra, augue arcu dictum risus, vel mollis nibh sapien id diam. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec sagittis nibh. Aliquam quis magna quam. Maecenas accumsan, enim vel varius sodales, massa libero placerat neque, id elementum nunc massa nec tortor. Nam vehicula orci quis libero pellentesque vestibulum.</p> \n                        <ul>\n                            <li>Lorem ipsum dolor</li>\n                            <li>Lorem ipsum dolor sit</li>\n                            <li>Lorem ipsum dolor sit amet</li>\n                            <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit</li>\n                        </ul>\n                    </div>\n                    <div class=\"article-paragraph\">\n                        <h3>Article heading 4</h3>\n                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras magna mi, fermentum vel metus vel, varius accumsan diam. Morbi mattis, velit eget venenatis pulvinar, odio dui interdum eros, eget egestas justo mi sit amet lorem. Donec venenatis, felis et volutpat viverra, augue arcu dictum risus, vel mollis nibh sapien id diam. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec sagittis nibh. Aliquam quis magna quam. Maecenas accumsan, enim vel varius sodales, massa libero placerat neque, id elementum nunc massa nec tortor. Nam vehicula orci quis libero pellentesque vestibulum.</p> \n                        <img src=\"/static/img/placeholder-wide.png\" class=\"img-fluid mx-auto d-block\">\n                    </div>\n                "}
    topics = ["Gaming", "Software", "Online", "Mobile", "Physical Security"]
    summary = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."

    @classmethod
    def populate_articles(cls, db, count=10):
        for i in range(count):
            author = Utilities.get_random_string(10)
            new_article = Article(
                author=author,
                title=f"Article {i} {Utilities.get_random_string(10)}",
                summary=cls.summary,
                content=json.dumps(cls.article_json),
                topic=random.choice(cls.topics),
                image_url=url_for("static", filename="img/placeholder.png")
            )
            db.session.add(new_article)
        db.session.commit()

    @classmethod
    def populate_lessons(cls, db, count): 
        for i in range(count): 
            author = Utilities.get_random_string(10)
            new_lesson = Lesson(
                author=author,
                title=f"Lesson {i} {Utilities.get_random_string(10)}",
                summary=cls.summary,
                topic=random.choice(cls.topics),
                content=json.dumps(cls.article_json),
            )

            #randomly choose a lesson to have questions
            if random.randint(0, 1): 
                new_lesson.questions=json.dumps(Utilities.generate_questions(5, 10))
                new_lesson.badge=Utilities.get_random_string(5)
                new_lesson.badge_url=url_for("static", filename="img/placeholder.png")

            db.session.add(new_lesson) 
        db.session.commit()

class Utilities:
    @staticmethod
    @app.template_filter()
    def regex_replace(string, find, replace):
        return re.sub(find, replace, string)

    @staticmethod
    @app.template_filter()
    def format_name(name):
        return name.lower().replace(' ', '_')

    @staticmethod
    def get_random_string(length=10):
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    @staticmethod
    def generate_questions(question_count, answer_count):
        result = {}

        for i in range(random.randint(1, question_count)):
            result.update({
                f"question_{i}":{
                    "value":Utilities.get_random_string(10),
                    "answers": Utilities.generate_answers(answer_count)
                }})
                
        return result

    @staticmethod
    def generate_answers(answer_count):
        result = {}
        for i in range(random.randint(2, answer_count)):
            result.update({f"answer_{i}":{"value":Utilities.get_random_string(10), "answer":bool(random.randint(0, 1))}})

        return result
        
