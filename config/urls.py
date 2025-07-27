from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('mealrater.urls', namespace='api')),
    path('auth-token/', include('rest_framework.urls')),
]

