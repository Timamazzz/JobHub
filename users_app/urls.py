import social_django
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users_app.views import UserViewSet, VKLoginView

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('api/auth/social/vk/', VKLoginView.as_view(), name='vk-login'),
    path('social/', include('social_django.urls')),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
