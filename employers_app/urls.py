from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from employers_app.views import EmployerViewSet, SendToModerationAPIView

router = DefaultRouter()
router.register(r'', EmployerViewSet)

urlpatterns = [
    path('send-to-moderation/', SendToModerationAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]
