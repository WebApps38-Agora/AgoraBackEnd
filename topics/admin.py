from django.contrib import admin
from topics.models import Topic, Article, Source

# Register your models here.
admin.site.register(Topic)
admin.site.register(Article)
admin.site.register(Source)
