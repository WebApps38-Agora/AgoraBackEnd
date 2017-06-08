import requests
import os
from topics.models import Article, Source
from collections import defaultdict

NEWS_API_KEY = os.environ['NEWS_API_KEY']
NEWS_API_ARTICLES = 'https://newsapi.org/v1/articles'
NEWS_API_SOURCES = 'https://newsapi.org/v1/sources'

class NewsApiError(Exception):
    pass


def get_newest_articles(source, sort_by='top'):
    '''Returns a list of the latest articles for a given source.

    The source argument is an identifier string such as 'bbc-news'.

    The sort_by argument is one of the following strings.
    top:     Sorted in the order they appear on the source's homepage.
    latest:  Sorted in chronological order, newest first.
    popular: Current most popular or currently trending headlines.'''

    params = {
        'source': source,
        'sortBy': sort_by,
        'apiKey': NEWS_API_KEY
    }

    response = requests.get(NEWS_API_ARTICLES, params=params).json()
    if response['status'] == 'ok':
        return response['articles']
    else:
        raise NewsApiError('Could not fetch articles for source {}, have you '
                           'set the NEWS_API_KEY environment variable?'.format(source))


def get_all_sources(language='en'):
    params = {
        'language': language
    }

    response = requests.get(NEWS_API_SOURCES, params=params)
    return response.json()['sources']


def update_article_database(allowed_source_ids):
    '''Queries the News API for latest articles, discovering new ones and adding
    them to the database.'''

    new_articles = []
    news_sources = get_all_sources()
    for source in news_sources:
        if source['id'] not in allowed_source_ids:
            continue

        s, _ = Source.objects.get_or_create(id=source['id'],
                                            name=source['name'],
                                            url=source['url'],
                                            description=source['description'],
                                            url_logo=get_source_logo(source['url']))
        articles = get_newest_articles(s.id)

        for article in articles:
            a, created = Article.objects.get_or_create(
                            url=article['url'],
                            defaults={'headline': article['title'],
                                      'description': article['description'],
                                      'url_image': article['urlToImage'],
                                      'published_at': article['publishedAt'],
                                      'source': s})
            if created:
                new_articles.append(a)

    return new_articles

def get_source_logo(url):
    return 'https://icons.better-idea.org/icon?url={}&size=70..120..200'.format(url)
