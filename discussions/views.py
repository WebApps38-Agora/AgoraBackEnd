from rest_framework import viewsets

from discussions.models import Comment
from discussions.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Retrieve the stored comments for a given topic.
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        if 'topic_id' in self.kwargs:
            return Comment.objects.filter(topic__id=self.kwargs['topic_id'])
        else:
            return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
