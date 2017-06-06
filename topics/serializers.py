from rest_framework import serializers
from topics.models import Article, Source, Topic


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Article
        fields = (
            "id",
            "headline",
            "description",
            "content",
            "url",
            "url_image",
            "published_at",

            "source",
            "topic",
        )


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = (
            "id",
            "name",
            "article_set",
            "url",
            "url_logo",
        )


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Topic
        fields = (
            "id",
            "article_set",
            "title",
            "published_at",
            "views",
        )
