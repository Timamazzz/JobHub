from django.urls import path, include
from rest_framework.routers import DefaultRouter

from job_openings_app.views import JobOpeningViewSet

router = DefaultRouter()
router.register(r'', JobOpeningViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
