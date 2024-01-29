from django.urls import path, include
from rest_framework.routers import DefaultRouter

from feed_app.views import EventViewSet, ExcursionViewSet, UsefulResourceViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'excursions', ExcursionViewSet)
router.register(r'useful-resources', UsefulResourceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
