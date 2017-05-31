import requests
import os
from topics.models import Article, Source

NEWS_API_KEY = os.environ['NEWS_API_KEY']
NEWS_API_ARTICLES = 'https://newsapi.org/v1/articles'
NEWS_API_SOURCES = 'https://newsapi.org/v1/sources'

def get_newest_articles(source, sort_by='latest'):
    '''Returns a list of the latest articles for a given source.

    The source argument is an identifier string such as 'bbc-news'.

    The sort_by argument is one of the following strings.
    top:     Sorted in the order they appear on the source's homepage.
    latest:  Sorted in chronological order, newest first.
    popular: Current most popular or currently trending headlines.'''

    params = {
        'source': source,
        'sortBy': sortBy,
        'apiKey': NEWS_API_KEY
    }

    response = requests.get(NEWS_API_ARTICLES, params=params).json()
    return response['articles'] if response['status'] == 'ok' else []


def get_all_sources(language='en'):
    '''Returns a list of source identifiers available on the News API,
    for the given language code, e.g. 'en'.'''

    params = {
        'language': language
    }

    response = requests.get(NEWS_API_SOURCES, params=params)
    return response.json()['sources']


def update_article_database():
    '''Queries the News API for latest articles, discovering new ones and adding
    them to the database.'''

    for source in get_all_sources():
        s, _ = Paper.objects.get_or_create(id=source['id'])
        articles = get_newest_articles(s.id)

        for article in articles:
            a, _ = Article.objects.get_or_create(
                            url=article['url'],
                            defaults={'headline': article['title'],
                                      'description': article['description']),
                                      'url_image': article['urlToImage'],
                                      'paper': s})
            a.save()
