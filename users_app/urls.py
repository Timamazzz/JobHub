import social_django
from django.urls import path, include, get_resolver
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users_app.views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('social/', include('social_django.urls')),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]

resolver = get_resolver()
for pattern in resolver.url_patterns:
    print(pattern)