from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('meals', views.MealViewSet)
router.register('ratings', views.RatingViewSet)
router.register('users', views.UserViewSet)
router.register('favorites', views.FavoriteViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls), name='mealratings_api'),
    path('obtain-token/', obtain_auth_token, name='obtain_token'),
]

