from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, TitleViewsSet, GenreViewsSet, CategoryViewsSet

from .views import auth, signup

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register('titles', TitleViewsSet, basename='title')
router.register('genres', GenreViewsSet, basename='genre')
router.register('categories', CategoryViewsSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', auth, name='auth'),
]
