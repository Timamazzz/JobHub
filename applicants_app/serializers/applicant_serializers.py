from rest_framework import serializers

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

    class Meta:
        model = Applicant
        fields = ('avatar', 'fio', 'birth_date', 'phone_number', 'email', 'resume')
