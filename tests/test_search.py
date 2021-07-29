from test_base import BaseTestCase
from app.models import Article, Lesson

class SearchUnitTests(BaseTestCase): 
    def test_search(self): 
        lesson = Lesson(
            author="username",
            topic="lesson_topic"
        )

        article = Article(
            author="username",
            topic="article_topic",
            image_url="url"
        )

        self.db.session.add(lesson)
        self.db.session.add(article)
        self.db.session.commit()
        
        response = self.app.post("/search", data=dict(
            query="topic"
        ), follow_redirects=True)

        self.assertIn(b"lesson_topic", response.data)
        self.assertIn(b"article_topic", response.data)