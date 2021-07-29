from test_base import BaseTestCase
from app.models import Article

class ArticleUnitTests(BaseTestCase): 
    def test_article_listing(self): 
        article = Article(
            author="username",
            image_url="image_url",
            topic="topic"
        )

        self.db.session.add(article) 
        self.db.session.commit()


        response = self.app.get("/news", follow_redirects=True)
        self.assertNotIn(b"No articles found", response.data) 