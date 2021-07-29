from test_base import BaseTestCase

from app.models import (
    User,
    Article,
    Lesson
)

class ModelUnitTests(BaseTestCase):
    def test_user_model(self):
        user = User(
            username="username",
            email="email@testing.com",
            password="Password1!"
        )

        self.assertEqual(user.username, "username")
        self.assertEqual(user.email, "email@testing.com")
        self.assertNotEqual(user.password_hash, "Password1!")

        self.db.session.add(user) 
        self.db.session.commit() 

        result = User.query.filter_by(username="username").first() 
        self.assertIsNotNone(result)

    def test_article_model(self): 
        article = Article(
            author="username",
            image_url="image_url",
            topic="topic"
        )

        self.assertIsNotNone(article.summary) 
        self.assertIsNotNone(article.content)

        self.db.session.add(article)
        self.db.session.commit() 

        result = Article.query.filter_by(author="username").first()
        self.assertIsNotNone(result)

    def test_lesson_model(self): 
        lesson = Lesson(
            author="author",
            title="lesson_title",
            topic="topic"
        )

        self.assertIsNotNone(lesson.content)
        self.assertIsNotNone(lesson.summary)

        self.db.session.add(lesson) 
        self.db.session.commit() 

        result = Lesson.query.filter_by(author="author").first()
        self.assertIsNotNone(result)