from django.test import TestCase
from topics.models import Article, Paper, Topic


class ArticleTest(TestCase):

    def setUp(self):
        self.p = Paper(name="The Test Paper")
        self.p.save()
        self.a1 = Article(headline="Test1", url="www.test.com", paper=self.p)
        self.a2 = Article(headline="Test2", url="www.test.com", paper=self.p)
        self.a1.save()
        self.a2.save()

    def test_article_can_have_more_than_one_topic(self):
        t1 = Topic(title="t1")
        t2 = Topic(title="t2")
        t1.save()
        t2.save()

        self.a1.topics.add(t1)
        self.a1.topics.add(t2)
