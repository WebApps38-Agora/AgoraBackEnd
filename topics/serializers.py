from rest_framework import serializers
from rest_framework.reverse import reverse
from topics.models import Article, Source, Topic


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    metrics = serializers.SerializerMethodField()

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
            "metrics",

            "source",
            "topic",
        )

    def get_metrics(self, obj):
        return reverse(
            'metrics-detail',
            args=[obj.id],
            request=self.context.get("request")
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
            "ranking",
        )
