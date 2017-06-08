#!python

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agora.settings")
django.setup()

from topics import newsapi
from topics import semantic

sources = ['bbc-news', 'the-guardian-uk', 'daily-mail', 'cnn', 'the-new-york-times']

for source in sources:
    new_articles = newsapi.update_article_database([source])
    semantic.create_topics(new_articles)
