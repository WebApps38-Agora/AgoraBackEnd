from rest_framework import serializers
from topics.models import Article, Paper, Topic


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


class PaperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paper
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
