from django.conf.urls import url, include
from rest_framework import routers

from metrics import views as metric_views
from topics import views as topic_views

router = routers.DefaultRouter()
router.register(r'articles', topic_views.ArticleViewSet)
router.register(r'papers', topic_views.PaperViewSet)
router.register(r'topics', topic_views.TopicViewSet)
router.register(r'reactions', metric_views.ReactionViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
]
