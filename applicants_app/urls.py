from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applicants_app.views import ApplicantViewSet

router = DefaultRouter()
router.register(r'', ApplicantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
