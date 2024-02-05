import secrets

import requests
import vk_api
from django.contrib.auth import login
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from JobHub.settings import SOCIAL_AUTH_VK_OAUTH2_KEY, SOCIAL_AUTH_VK_OAUTH2_SECRET
from JobHub.utils.ModelViewSet import ModelViewSet
from applicants_app.models import Applicant
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
        return redirect(
            'https://oauth.vk.com/authorize?client_id=51846722&redirect_uri=http://51.250.126.124:8099/'
            'api/users/vk-login/callback&display=page')

    @action(detail=False, methods=['GET'], url_path='vk-login/callback')
    def vk_login_callback(self, request):
        code = request.GET.get('code')
        if not code:
            return redirect('path_to_error_page')

        response = requests.get('https://oauth.vk.com/access_token', params={
            'client_id': SOCIAL_AUTH_VK_OAUTH2_KEY,
            'client_secret': SOCIAL_AUTH_VK_OAUTH2_SECRET,
            'redirect_uri': 'http://51.250.126.124:8099/',
            'code': code
        })
        data = response.json()
        access_token = data.get('access_token')
        print('data:', data)

        vk_user_id = data.get('user_id')

        # Используйте vk_api для получения информации о пользователе
        vk_session = vk_api.VkApi(token=access_token)
        vk = vk_session.get_api()
        user_info = vk.users.get(user_ids=vk_user_id, fields='first_name,last_name,bdate')

        first_name = user_info[0]['first_name']
        last_name = user_info[0]['last_name']
        birth_date = user_info[0].get('bdate')

        applicant_profile, created = Applicant.objects.get_or_create(
            vk_id=vk_user_id,
            defaults={
                'fio': f'{first_name} {last_name}',
                'birth_date': birth_date,
            }
        )

        print('applicant_profile:', applicant_profile)
        log = login(request, applicant_profile.user)
        print('login:', log)

        if created:
            return redirect('/profile')
        else:
            return redirect('/')
