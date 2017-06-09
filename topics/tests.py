from django.test import TestCase
from rest_framework.test import APIClient
from topics.models import Article, Topic

import topics.newsapi as newsapi
import topics.semantic as semantic


class APITest(TestCase):

    entry_points = ["articles", "sources", "topics"]

    def test_user_cannot_do_unsafe_requests(self):
        userclient = APIClient()

        for entry_point in self.entry_points:
            self.assertEqual(
                userclient.delete(
                    '/{}/1/'.format(entry_point)
                ).status_code, 401)
            self.assertEqual(
                userclient.post(
                    '/{}/'.format(entry_point), {}
                ).status_code, 401)
            self.assertEqual(
                userclient.patch(
                    '/{}/1/'.format(entry_point), {}
                ).status_code, 401)


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
        self.articles = [None]*7
        self.articles[0] = Article(headline='Theresa May calls snap election')
        self.articles[1] = Article(headline='Theresa May announces snap election')
        self.articles[2] = Article(headline='May surprises the UK with an election')
        self.articles[3] = Article(headline='Turkish president accused of fabricating army coup')
        self.articles[4] = Article(headline='Recent Turkish coup to strengthen Erdogan\'s position')
        self.articles[5] = Article(headline='Turkish mafia on the rise')
        self.articles[6] = Article(headline='The UK to leave the european union')
        for article in self.articles:
            article.save()

    def test_topics_created(self):
        semantic.create_topics(self.articles)
        topics = Topic.objects.all()
        articles = Article.objects.all()

        # There are 4 topics created, each one having the title of the first relvant article
        self.assertEqual(Topic.objects.count(), 4)
        self.assertEqual(topics[0].title, 'Theresa May calls snap election')
        self.assertEqual(topics[1].title, 'Turkish president accused of fabricating army coup')
        self.assertEqual(topics[2].title, 'Turkish mafia on the rise')
        self.assertEqual(topics[3].title, 'The UK to leave the european union')

        # Theresa May election articles grouped together
        self.assertEqual(articles[0].topic, topics[0])
        self.assertEqual(articles[1].topic, topics[0])
        self.assertEqual(articles[2].topic, topics[0])

        # Turkish coup articles grouped together
        self.assertEqual(articles[3].topic, topics[1])
        self.assertEqual(articles[4].topic, topics[1])

        # The rest are seperate topics
        self.assertEqual(articles[5].topic, topics[2])
        self.assertEqual(articles[6].topic, topics[3])


    def test_topics_updated(self):
        self.test_topics_created()

        new_articles = [
            Article(headline='Snap election might blow up in Theresa\'s face'),
            Article(headline='Erdogan calls recent army coup a hoax'),
            Article(headline='Computing student salaries are through the roof'),
        ]

        for article in new_articles:
            article.save()

        semantic.create_topics(new_articles)

        topics = Topic.objects.all()
        articles = Article.objects.all()

        # Add Theresa May article to existing topic
        self.assertEqual(articles[7].topic, topics[0])

        # Add Erdogan article to existing topic
        self.assertEqual(articles[8].topic, topics[1])

        # Add Computing article to new topic
        self.assertEqual(len(topics), 5)
        self.assertEqual(articles[9].topic, topics[4])
