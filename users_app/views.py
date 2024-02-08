import json
import uuid
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
from JobHub.settings import SOCIAL_AUTH_VK_OAUTH2_KEY, SOCIAL_AUTH_VK_OAUTH2_SECRET, AFTER_VK_AUTH_REDIRECT_REGISTER, \
    AFTER_VK_AUTH_REDIRECT_LOGIN
from JobHub.utils.FileUploadView import save_uploaded_files
from JobHub.utils.ModelViewSet import ModelViewSet
from JobHub.utils.fields import formate_phone
from applicants_app.models import Applicant
from docs_app.models import ApplicantAvatar
from users_app.enums import UserRoleEnum
from users_app.models import User
from users_app.serializers.user_serializers import UserSerializer, UserRetrieveSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users_app.utils import get_user_data


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
        uuid_str = str(uuid.uuid4())
        app_id = SOCIAL_AUTH_VK_OAUTH2_KEY
        redirect_state = 'your_app_state'

        scopes = ['phone_number', 'email']
        scope_param = ','.join(scopes)

        query = f'uuid={uuid_str}&app_id={app_id}&response_type=silent_token&redirect_uri={redirect_uri}&redirect_state={redirect_state}'
        vk_auth_url = f'https://id.vk.com/auth?{query}'

        #vk_auth_url = f'https://oauth.vk.com/authorize?client_id=51846722&redirect_uri={redirect_uri}&display=page&scope={scope_param}'

        response_data = {'vk_auth_url': vk_auth_url}
        return JsonResponse(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='vk-login/callback', name='vk-login-callback')
    def vk_login_callback(self, request):
        code = request.GET.get('code')
        payload_str = request.GET.get('payload', None)
        payload = json.loads(payload_str) if payload_str else None

        vk_user_id, domain, photo, email, first_name, last_name, birth_date, phone_number = get_user_data(request,
                                                                                                          code=code,
                                                                                                          payload=payload)

        if domain and email:
            with transaction.atomic():
                user, created = User.objects.get_or_create(
                    username=domain,
                    email=email,
                    defaults={
                        'role': UserRoleEnum.APPLICANT.name,
                    }
                )

                if created:
                    applicant_email = email if email else None
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
                                    file=file_data['file'],
                                    original_name=file_data['original_name'],
                                    extension=file_data['extension']
                                )

                                applicant_profile.avatar = applicant_avatar
                                applicant_profile.save()

                            except Exception as e:
                                return HttpResponseServerError("Internal Server Error")

                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token

                    if created:
                        return redirect(
                            f'{AFTER_VK_AUTH_REDIRECT_REGISTER}?access_token={access_token}&refresh_token={refresh}')
                    else:
                        return redirect(
                            f'{AFTER_VK_AUTH_REDIRECT_LOGIN}?access_token={access_token}&refresh_token={refresh}')

        return HttpResponse({}, status=status.HTTP_200_OK)
