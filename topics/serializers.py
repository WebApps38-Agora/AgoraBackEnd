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
            "paper",
            "topics",
        )


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = (
            "name",
            "article_set",
        )


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = (
            "title",
            "date",
            "article_set",
        )
