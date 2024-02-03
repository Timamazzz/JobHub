import secrets

from django.contrib.auth import login
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from JobHub.settings import SOCIAL_AUTH_VK_OAUTH2_KEY
from JobHub.utils.ModelViewSet import ModelViewSet
from users_app.models import User
from users_app.serializers.user_serializers import UserSerializer, UserRetrieveSerializer
from social_django.utils import load_backend, load_strategy, psa


# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_list = {
        'retrieve': UserRetrieveSerializer,
    }

    @staticmethod
    def generate_random_string(length=32):
        return secrets.token_urlsafe(length)

    # @action(detail=False, methods=['GET'], url_path='vk-login')
    # def vk_login(self, request):
    #     print('request.build_absolute_uri("/")[:-1]', request.build_absolute_uri("/")[:-1])
    #     redirect_uri = F'{request.build_absolute_uri("/")[:-1]}/api/users/vk-login/callback/'
    #     redirect_uri += f'?backend=vk-oauth2'
    #
    #     state = 'state'
    #     request.session['vk_login_state'] = state
    #     redirect_uri += f'&state={state}'
    #
    #     scope = ['email']
    #
    #     authorize_url = (f'https://oauth.vk.com/authorize?client_id={SOCIAL_AUTH_VK_OAUTH2_KEY}&'
    #                      f'redirect_uri={redirect_uri}&response_type=code&scope={",".join(scope)}')
    #
    #     return redirect(authorize_url)
    #
    # @action(detail=False, methods=['GET'], url_path='vk-login/callback')
    # def vk_login_callback(self, request):
    #     try:
    #         strategy = load_strategy(request)
    #         backend = load_backend(strategy, 'vk-oauth2', redirect_uri=f'http://rabota.belregion.ru/')
    #
    #         code = request.query_params.get('code')
    #
    #         state = request.query_params.get('state')
    #
    #         if state != 'state':
    #             return HttpResponseBadRequest('Wrong state parameter given.')
    #
    #         user = backend.complete(strategy, response_data={'code': code, 'state': state})
    #
    #         if user:
    #             login(request, user)
    #             return Response({'detail': 'VK login successful'}, status=status.HTTP_200_OK)
    #         else:
    #             return HttpResponseBadRequest('VK login failed')
    #     except Exception as e:
    #         return HttpResponseBadRequest(f'Error during VK login: {str(e)}')

    @action(detail=False, methods=['GET'], url_path='vk-login')
    def vk_login(self, request):
        return redirect('social:begin', 'vk-oauth2')

    @action(detail=False, methods=['GET'], url_path='vk-login/callback')
    def vk_login_callback(self, request):
        print(('hello'))
        user = request.backend.do_auth(request.backend.strategy, request.backend.data)
        if user:
            login(request, user)
            return Response({'detail': 'VK login successful'})
        else:
            return HttpResponseBadRequest('VK login failed')