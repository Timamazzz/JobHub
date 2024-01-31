from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('social/', include('social_django.urls')),
    path('', include(router.urls)),
]
