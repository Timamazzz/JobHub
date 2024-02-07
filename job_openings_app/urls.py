from django.urls import path, include
from rest_framework.routers import DefaultRouter

from employers_app.views import SendToModerationAPIView
from job_openings_app.views import JobOpeningViewSet, JobCategoryViewSet, JobActivityViewSet

router = DefaultRouter()
router.register(r'categories', JobCategoryViewSet)
router.register(r'activities', JobActivityViewSet)
router.register(r'', JobOpeningViewSet)


urlpatterns = [
    path('a/send-to-moderation/', SendToModerationAPIView.as_view()),
    path('', include(router.urls)),
]
