from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applicants_app.views import ApplicantViewSet

router = DefaultRouter()
router.register(r'', ApplicantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

routes = router.get_routes(ApplicantViewSet)
action_list = []
for route in routes:
    action_list += list(route.mapping.values())
distinct_action_list = set(action_list)
print('action_list', distinct_action_list)
