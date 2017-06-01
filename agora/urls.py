from django.conf.urls import url, include
from rest_framework import routers

from metrics import views as metric_views
from topics import views as topic_views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'articles', topic_views.ArticleViewSet)
router.register(r'sources', topic_views.SourceViewSet)
router.register(r'topics', topic_views.TopicViewSet)
router.register(r'reactions', metric_views.ReactionViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(
        r'^metrics/articles/(?P<article>[0-9]+)/$',
        metric_views.ArticleMetricsAPIView.as_view()
    ),
    url(r'^admin/', admin.site.urls),
    url(r'^update_news/', topic_views.UpdateNews.as_view())
]
