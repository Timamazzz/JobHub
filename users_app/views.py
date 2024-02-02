from django.http import JsonResponse
from django.views import View
from social_django.utils import psa

from JobHub.utils.ModelViewSet import ModelViewSet
from users_app.models import User
from users_app.serializers.user_serializers import UserSerializer, UserRetrieveSerializer


# Create your views here.
class VKLoginView(View):
    @psa('social:begin', 'vk-login')
    def get(self, request, *args, **kwargs):
        print('request.backend.auth_url()', request.backend.auth_url())
        return self.render_json_response({'redirect_url': request.backend.auth_url()})

    def render_json_response(self, data, status=200):
        print('data', data)
        return JsonResponse(data, status=status)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_list = {
        'retrieve': UserRetrieveSerializer,
    }
