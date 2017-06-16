#!python

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agora.settings")
django.setup()

from topics import newsapi
from topics import semantic
from topics.models import Topic

sources = [
    'bbc-news',
    'the-guardian-uk',
    'daily-mail',
    'cnn',
    'the-new-york-times',
    'al-jazeera-english',
    'bloomberg',
    'breitbart-news',
    'independent',
    'metro',
    'the-huffington-post',
    'the-telegraph',
    'the-wall-street-journal',
    'the-washington-post',
    'usa-today',
]

for source in sources:
    new_articles = newsapi.update_article_database([source])
    for article in new_articles:
        semantic.create_topics([article])

Topic.update_rankings()
