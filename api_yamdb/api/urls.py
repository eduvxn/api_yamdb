from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import titleViewsSet, categoryViewsSet, genreViewsSet

app_name = 'api'

router = SimpleRouter()
router.register('titles', titleViewsSet, basename='title')
router.register('genres', genreViewsSet, basename='genre')
router.register('categories', categoryViewsSet, basename='category')

urlpatterns = [
    path('v1/', include(router.urls))
]
