from django.test import TestCase
from rest_framework.test import APIClient

from topics.models import Article, Source, Topic
import newsapi


class ArticleTest(TestCase):

    def setUp(self):
        self.p = Source(name="The Test Paper")
        self.p.save()
        self.a1 = Article(headline="Test1", url="www.test.com", source=self.p)
        self.a2 = Article(headline="Test2", url="www.test.com", source=self.p)
        self.a1.save()
        self.a2.save()

    def test_article_can_have_more_than_one_topic(self):
        t1 = Topic(title="t1")
        t2 = Topic(title="t2")
        t1.save()
        t2.save()

        self.a1.topics.add(t1)
        self.a1.topics.add(t2)


class APITest(TestCase):

    entry_points = ["articles", "papers", "topics"]

    def test_user_cannot_do_unsafe_requests(self):
        userclient = APIClient()

        for entry_point in self.entry_points:
            assert(
                userclient.delete(
                    '/{}/1/'.format(entry_point)
                ).status_code == 403
            )
            assert(
                userclient.post(
                    '/{}/'.format(entry_point), {}
                ).status_code == 403
            )
            assert(
                userclient.patch(
                    '/{}/1/'.format(entry_point), {}
                ).status_code == 403
            )


class NewsApiTest(TestCase):

    def test_returns_some_sources(self):
        sources = newsapi.get_all_sources()
        self.assertGreater(len(sources), 0)

    def test_returns_some_articles(self):
        articles = newsapi.get_newest_articles('bbc-news')
        self.assertGreater(len(articles), 0)

    def test_new_articles_populate_database(self):
        self.assertEqual(len(Article.objects.all()), 0)
        newsapi.update_article_database(['bbc-news'])
        self.assertGreater(len(Article.objects.all()), 0)

    def test_old_articles_do_not_get_added(self):
        newsapi.update_article_database(['bbc-news'])
        previous = len(Article.objects.all())

        newsapi.update_article_database(['bbc-news'])
        new = len(Article.objects.all())
        self.assertEqual(previous, new)
