from django.conf.urls import url, include
from rest_framework import routers

from metrics import views as metric_views
from topics import views as topic_views
from facts import views as fact_views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'articles', topic_views.ArticleViewSet)
router.register(r'sources', topic_views.SourceViewSet)
router.register(r'topics', topic_views.TopicViewSet)
router.register(
    r'metrics', metric_views.ArticleMetricsViewSet, base_name="metrics"
)
router.register(r'facts', fact_views.FactViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url('^facts/topic/(?P<topic_id>[0-9]+)/$', fact_views.FactViewSet.as_view({'get': 'list'})),
]
