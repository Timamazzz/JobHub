from datetime import datetime
import requests
import vk_api
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import transaction
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import action
from JobHub.settings import SOCIAL_AUTH_VK_OAUTH2_KEY, SOCIAL_AUTH_VK_OAUTH2_SECRET
from JobHub.utils.FileUploadView import save_uploaded_files
from JobHub.utils.ModelViewSet import ModelViewSet
from JobHub.utils.fields import formate_phone
from applicants_app.models import Applicant
from docs_app.models import ApplicantAvatar
from users_app.enums import UserRoleEnum
from users_app.models import User
from users_app.serializers.user_serializers import UserSerializer, UserRetrieveSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_list = {
        'retrieve': UserRetrieveSerializer,
    }

    @action(detail=False, methods=['GET'], url_path='vk-login')
    def vk_login(self, request):
        my_domain = request.build_absolute_uri('/')[:-1]
        redirect_uri = f'{my_domain}/api/users/vk-login/callback'

        scopes = ['phone_number', ]
        scope_param = ','.join(scopes)

        vk_auth_url = f'https://oauth.vk.com/authorize?client_id=51846722&redirect_uri={redirect_uri}&display=page&scope={scope_param}'

        response_data = {'vk_auth_url': vk_auth_url}
        return JsonResponse(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='vk-login/callback', name='vk-login-callback')
    def vk_login_callback(self, request):
        code = request.GET.get('code')
        if not code:
            return HttpResponse

        my_domain = request.build_absolute_uri('/')[:-1]
        redirect_uri = f'{my_domain}/api/users/vk-login/callback'

        response = requests.get('https://oauth.vk.com/access_token', params={
            'client_id': SOCIAL_AUTH_VK_OAUTH2_KEY,
            'client_secret': SOCIAL_AUTH_VK_OAUTH2_SECRET,
            'redirect_uri': redirect_uri,
            'code': code
        })

        data = response.json()
        access_token = data.get('access_token')

        vk_user_id = data.get('user_id')

        vk_session = vk_api.VkApi(token=access_token)
        vk = vk_session.get_api()
        user_info = vk.users.get(user_ids=vk_user_id, fields='first_name,last_name,bdate,contacts,domain,photo_200')

        first_name = user_info[0]['first_name']
        last_name = user_info[0]['last_name']
        birth_date = datetime.strptime(user_info[0].get('bdate'), '%d.%m.%Y').strftime('%Y-%m-%d')
        phone_number = formate_phone(user_info[0].get('mobile_phone'))
        domain = user_info[0].get('domain')
        photo = user_info[0].get('photo_200')

        email = data.get('email') if data.get('email') is not None else f'{vk_user_id}@mail.com'
        applicant_email = data.get('email') if data.get('email') is not None else None

        with transaction.atomic():
            user, created = User.objects.get_or_create(
                username=domain,
                email=email,
                defaults={
                    'role': UserRoleEnum.APPLICANT.name,
                }
            )

            applicant_profile, created = Applicant.objects.get_or_create(
                user=user,
                vk_id=vk_user_id,
                defaults={
                    'fio': f'{first_name} {last_name}',
                    'birth_date': birth_date,
                    'phone_number': phone_number,
                    'email': applicant_email,
                }
            )

            if created and photo:
                avatar_file_data = save_uploaded_files([photo])
                for file_data in avatar_file_data:
                    try:
                        applicant_avatar = ApplicantAvatar.objects.create(
                            applicant=applicant_profile,
                            file=file_data['url'],
                            original_name=file_data['original_name'],
                            extension=file_data['extension']
                        )
                    except Exception as e:
                        return HttpResponseServerError("Internal Server Error")

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            if created:
                return redirect(f'http://localhost:3000/profile?access_token={access_token}&refresh_token={refresh}')
            else:
                return redirect(f'http://localhost:3000/?access_token={access_token}&refresh_token={refresh}')

        return HttpResponse({}, status=status.HTTP_200_OK)
