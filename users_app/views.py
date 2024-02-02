from django.contrib.auth import login
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from social_django.utils import psa

from JobHub.settings import SOCIAL_AUTH_VK_OAUTH2_KEY
from JobHub.utils.ModelViewSet import ModelViewSet
from users_app.models import User
from users_app.serializers.user_serializers import UserSerializer, UserRetrieveSerializer
from social_django.utils import load_backend, load_strategy


# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_list = {
        'retrieve': UserRetrieveSerializer,
    }

    @action(detail=False, methods=['GET'], url_path='vk-login')
    def vk_login(self, request):
        print('request.build_absolute_uri("/")[:-1]', request.build_absolute_uri("/")[:-1])
        redirect_uri = F'{request.build_absolute_uri("/")[:-1]}/api/users/vk-login/callback/'
        redirect_uri += f'?backend=vk-oauth2'
        scope = ['email']

        authorize_url = (f'https://oauth.vk.com/authorize?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY}&'
                         f'redirect_uri={redirect_uri}&response_type=code&scope={",".join(scope)}')

        return redirect(authorize_url)

    @action(detail=False, methods=['GET'], url_path='vk-login/callback')
    def vk_login_callback(self, request):
        try:
            print('request', request)
            strategy = load_strategy(request)
            print('strategy', strategy)
            backend = load_backend(strategy, 'vk-oauth2', redirect_uri=None)
            print('backend', backend)
            user = backend.complete(strategy, response_data={})
            print('user', user)

            if user:
                login(request, user)
                return Response({'detail': 'VK login successful'}, status=status.HTTP_200_OK)
            else:
                return HttpResponseBadRequest('VK login failed')
        except Exception as e:
            print('error', e)
            return HttpResponseBadRequest(f'Error during VK login: {str(e)}')
