from rest_framework import serializers

from JobHub.utils.fields import PhoneField
from applicants_app.models import Applicant
from docs_app.serializers.ApplicantAvatarSerializer import ApplicantCreateAvatarSerializer, \
    ApplicantRetrieveAvatarSerializer


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantRetrieveSerializer(serializers.ModelSerializer):
    avatar = ApplicantRetrieveAvatarSerializer(many=False, read_only=True)

    class Meta:
        model = Applicant
        fields = ('avatar', 'fio', 'birth_date', 'phone_number', 'email', 'resume')


class ApplicantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantUpdateSerializer(serializers.ModelSerializer):
    avatar = ApplicantCreateAvatarSerializer(many=False)
    phone_number = PhoneField()

    class Meta:
        model = Applicant
        fields = ('avatar', 'fio', 'birth_date', 'phone_number', 'email', 'resume')
