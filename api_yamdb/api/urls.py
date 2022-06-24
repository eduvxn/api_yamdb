from rest_framework.routers import SimpleRouter

from django.urls import include, path

from .views import CommentViewSet, CommentsViewSet, ReviewViewSet

app_name = 'api'

router = SimpleRouter()

router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
]
