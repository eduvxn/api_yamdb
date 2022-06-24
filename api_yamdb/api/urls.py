
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TitleViewsSet, CategoryViewsSet, GenreViewsSet, CommentViewSet, CommentsViewSet, ReviewViewSet

app_name = 'api'

router = SimpleRouter()
# router.register(r'users', UserViewSet, basename='users')
router.register('titles', TitleViewsSet, basename='title')
router.register('genres', GenreViewsSet, basename='genre')
router.register('categories', CategoryViewsSet, basename='category')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/signup/', signup_view, name='registration'),
    # path('auth/token/', get_token_view, name='token'),
]
