from rest_framework import serializers

from applicants_app.models import Applicant


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ('fio', 'birth_date', 'phone_number', 'email', 'resume')


class ApplicantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        ffields = ('fio', 'birth_date', 'phone_number', 'email', 'resume')
