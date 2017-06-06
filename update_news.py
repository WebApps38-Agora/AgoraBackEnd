#!python

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agora.settings")
django.setup()

from topics import newsapi
from topics import semantic

newsapi.update_article_database(['bbc-news', 'the-guardian-uk', 'daily-mail'])
semantic.create_all_topics()
