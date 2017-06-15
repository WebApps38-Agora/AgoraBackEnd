from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

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
        comment = serializer.save(owner=self.request.user)

        # Automatically subscribe to your own comment
        comment.subscribers.add(self.request.user)

        # Notify all users subscribed to the parent comment
        if comment.parent_comment is not None:
            content = comment.parent_comment.content
            content = (content[:40] + "...") if len(content) > 40 else content

            comment.parent_comment.notify_all(
                notification_type="new_comment",
                relevant_id=comment.topic.id,
                content="New reply to {}".format(content),
                exclude=[self.request.user],
            )

    @detail_route()
    def subscribe(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.subscribers.add(request.user)

        return Response("Success")

    @detail_route()
    def unsubscribe(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.subscribers.remove(request.user)

        return Response("Success")
