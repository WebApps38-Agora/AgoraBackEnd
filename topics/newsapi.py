import requests
import os

NEWS_API_KEY = os.environ['NEWS_API_KEY']
NEWS_API_ARTICLES = 'https://newsapi.org/v1/articles'
NEWS_API_SOURCES = 'https://newsapi.org/v1/sources'

def get_articles(source, sortBy):
    params = {
        'source': source,
        'sortBy': sortBy,
        'apiKey': NEWS_API_KEY
    }

    response = requests.get(NEWS_API_ARTICLES, params=params).json()
    return response['articles'] if response['status'] == 'ok' else []

def get_sources(language='en'):
    params = {
        'language': language
    }

    response = requests.get(NEWS_API_SOURCES, params=params)
    return response.json()['sources']
