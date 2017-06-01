from django.test import TestCase
from rest_framework.test import APIClient
from topics.models import Article, Source, Topic

import topics.newsapi as newsapi
import topics.semantic as semantic

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

    entry_points = ["articles", "sources", "topics"]

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


class TopicsTest(TestCase):
    def setUp(self):
        self.s = Source(name="Some Paper")
        self.s.save()
        self.articles = [None]*7
        self.articles[0] = Article(url='1', headline="Theresa May calls snap election")
        self.articles[1] = Article(url='2', headline="Theresa May announces snap election")
        self.articles[2] = Article(url='3', headline="May surprises the UK with an election")
        self.articles[3] = Article(url='4', headline="Turkish president accused of fabricating army coup")
        self.articles[4] = Article(url='5', headline="Recent Turkish coup to strengthen Erdogan's position")
        self.articles[5] = Article(url='6', headline="Turkish mafia on the rise")
        self.articles[6] = Article(url='7', headline="The UK to leave the european union")
        for article in self.articles:
            article.source = self.s
            article.save()

    def test_topics_created(self):
        semantic.create_all_topics()
        topics = Topic.objects.all()

        # There are 4 topics created, each one having the title of the first relvant article
        self.assertEqual(Topic.objects.count(), 4)
        self.assertEqual(topics[0].title, 'Theresa May calls snap election')
        self.assertEqual(topics[1].title, 'Turkish president accused of fabricating army coup')
        self.assertEqual(topics[2].title, 'Turkish mafia on the rise')
        self.assertEqual(topics[3].title, 'The UK to leave the european union')

        # Theresa May election articles grouped together
        self.assertEqual(self.articles[0].topics.all()[0], topics[0])
        self.assertEqual(self.articles[1].topics.all()[0], topics[0])
        self.assertEqual(self.articles[2].topics.all()[0], topics[0])

        # Turkish coup articles grouped together
        self.assertEqual(self.articles[3].topics.all()[0], topics[1])
        self.assertEqual(self.articles[4].topics.all()[0], topics[1])

        # The rest are seperate topics
        self.assertEqual(self.articles[5].topics.all()[0], topics[2])
        self.assertEqual(self.articles[6].topics.all()[0], topics[3])
