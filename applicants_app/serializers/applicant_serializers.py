import traceback

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from JobHub.utils.fields import PhoneField
from applicants_app.models import Applicant
from docs_app.models import ApplicantAvatar
from docs_app.serializers.ApplicantAvatarSerializer import ApplicantCreateAvatarSerializer, \
    ApplicantRetrieveAvatarSerializer


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantRetrieveSerializer(serializers.ModelSerializer):
    avatar = ApplicantRetrieveAvatarSerializer()

    class Meta:
        model = Applicant
        fields = ('id', 'avatar', 'fio', 'birth_date', 'phone_number', 'email', 'resume')


class ApplicantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantUpdateSerializer(serializers.ModelSerializer):
    phone_number = PhoneField()


    class Meta:
        model = Applicant
        fields = ('avatar', 'fio', 'birth_date', 'phone_number', 'email', 'resume')


class ApplicantForJobOpeningsListSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Applicant
        fields = ('id', 'avatar_url')

    def get_avatar_url(self, obj):
        try:
            return obj.avatar.file.url
        except AttributeError:
            return None