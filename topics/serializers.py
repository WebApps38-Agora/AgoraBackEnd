from rest_framework import serializers
from rest_framework.reverse import reverse
from topics.models import Article, Source, Topic
from facts.serializers import FactSerializer
from discussions.serializers import CommentSerializer

class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = (
            "id",
            "name",
            "url",
            "url_logo",
        )


class NestedSourceSerializer(SourceSerializer):
    class Meta(SourceSerializer.Meta):
        fields = SourceSerializer.Meta.fields + ("article_set",)


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
    images = serializers.SlugRelatedField(
        source="article_set",
        many=True,
        read_only=True,
        slug_field="url_image",
    )

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "published_at",
            "images",
            "views",
            "ranking",
        )


class NestedTopicSerializer(TopicSerializer):
    article_set = ArticleSerializer(many=True)
    fact_set = FactSerializer(many=True)
    comment_set = CommentSerializer(many=True)

    class Meta(TopicSerializer.Meta):
        fields = TopicSerializer.Meta.fields + ("article_set", "fact_set", "comment_set")
