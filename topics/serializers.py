from rest_framework import serializers
from rest_framework.reverse import reverse
from topics.models import Article, Source, Topic
from facts.serializers import FactSerializer


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


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    metrics = serializers.SerializerMethodField()
    source = SourceSerializer()

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


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    article_set = ArticleSerializer(many=True)
    fact_set = FactSerializer(many=True)

    class Meta:
        model = Topic
        fields = (
            "id",
            "article_set",
            "fact_set",
            "title",
            "published_at",
            "views",
            "ranking",
        )
