from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from facts import views as fact_views
from metrics import views as metric_views
from topics import views as topic_views
from user_profile import views as profile_views
from notifications import views as notification_views
from discussions import views as discussion_views

router = routers.DefaultRouter()
router.register(r'articles', topic_views.ArticleViewSet)
router.register(r'sources', topic_views.SourceViewSet)
router.register(r'topics', topic_views.TopicViewSet)

router.register(
    r'metrics', metric_views.ArticleMetricsViewSet, base_name="metrics"
)
router.register(r'notifications', notification_views.NotificationViewSet)
router.register(r'facts', fact_views.FactViewSet)
router.register(r'fact_reactions', fact_views.FactReactionViewSet)
router.register(r'profiles', profile_views.ProfileViewSet)

router.register(r'comments', discussion_views.CommentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^rest_auth/', include('rest_auth.urls')),
    url(r'^rest_auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest_auth/facebook/$',
        topic_views.FacebookLogin.as_view(), name='fb_login'),
    url(r'^admin/', admin.site.urls),
    url('^facts/topic/(?P<topic_id>[0-9]+)/$',
        fact_views.FactViewSet.as_view({'get': 'list'})),
    url('^fact_reactions/fact/(?P<fact_id>[0-9]+)/$',
        fact_views.FactReactionViewSet.as_view({'get': 'list'})),
]
