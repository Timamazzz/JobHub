from rest_framework import serializers

from applicants_app.models import Applicant


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'
