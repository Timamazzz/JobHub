from django.urls import path, include
from rest_framework.routers import DefaultRouter
from job_openings_app.views import JobOpeningViewSet, JobCategoryViewSet, JobActivityViewSet

router = DefaultRouter()
router.register(r'', JobOpeningViewSet)
router.register(r'categories', JobCategoryViewSet)
router.register(r'activities', JobActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
