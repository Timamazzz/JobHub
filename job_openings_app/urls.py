from django.urls import path, include
from rest_framework.routers import DefaultRouter

from job_openings_app.views import JobOpeningViewSet, JobCategoryViewSet, JobActivityViewSet, WorkOnHolidayAPIView

router = DefaultRouter()
router.register(r'categories', JobCategoryViewSet)
router.register(r'activities', JobActivityViewSet)
router.register(r'', JobOpeningViewSet)


urlpatterns = [
    path('work-on-holiday/', WorkOnHolidayAPIView.as_view(), name='work-on-holiday'),
    path('', include(router.urls)),
]
