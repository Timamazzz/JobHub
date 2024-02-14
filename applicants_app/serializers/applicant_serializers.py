import traceback

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from JobHub.utils.fields import PhoneField
from applicants_app.models import Applicant
from docs_app.models import ApplicantAvatar
from docs_app.serializers.ApplicantAvatarSerializer import ApplicantCreateOrUpdateAvatarSerializer, \
    ApplicantRetrieveAvatarSerializer


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantListSerializer(serializers.ModelSerializer):
    avatar = ApplicantRetrieveAvatarSerializer()

    class Meta:
        model = Applicant
        fields = ('id', 'fio', 'birth_date', 'phone_number', 'email', 'resume', 'avatar')


class ApplicantRetrieveSerializer(WritableNestedModelSerializer):
    avatar = ApplicantRetrieveAvatarSerializer()

    class Meta:
        model = Applicant
        fields = ('id', 'avatar', 'fio', 'birth_date', 'phone_number', 'email', 'resume')


class ApplicantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantUpdateSerializer(WritableNestedModelSerializer):
    avatar = ApplicantCreateOrUpdateAvatarSerializer()
    phone_number = PhoneField()

    class Meta:
        model = Applicant
        fields = ('id', 'avatar', 'fio', 'birth_date', 'phone_number', 'email', 'resume')
        extra_kwargs = {
            'email': {'required': True}
        }


class ApplicantForJobOpeningsListSerializer(WritableNestedModelSerializer):
    avatar = serializers.CharField(source='avatar.file')

    class Meta:
        model = Applicant
        fields = ('id', 'fio', 'birth_date', 'phone_number', 'avatar')
