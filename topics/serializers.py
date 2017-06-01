from rest_framework import serializers
from topics.models import Article, Source, Topic


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = (
            "headline",
            "description",
            "content",
            "url",
            "source",
            "topics",
            "url_image"
        )


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = (
            "name",
            "article_set",
            "url",
            "url_logo"
        )


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = (
            "date",
            "article_set",
        )
