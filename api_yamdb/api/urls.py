from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (UserViewSet, TitleViewsSet,
                       GenreViewsSet, CategoryViewsSet,
                       CommentsViewSet, ReviewViewSet)

from .views import auth, signup


app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register('titles', TitleViewsSet, basename='title')
router.register('genres', GenreViewsSet, basename='genre')
router.register('categories', CategoryViewsSet, basename='category')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', auth, name='auth'),
]
