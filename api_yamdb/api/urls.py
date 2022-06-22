from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TitleViewsSet, CategoryViewsSet, GenreViewsSet

app_name = 'api'

router = SimpleRouter()
# router.register(r'users', UserViewSet, basename='users')
router.register('titles', TitleViewsSet, basename='title')
router.register('genres', GenreViewsSet, basename='genre')
router.register('categories', CategoryViewsSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    # path('auth/signup/', signup_view, name='registration'),
    # path('auth/token/', get_token_view, name='token'),
]
