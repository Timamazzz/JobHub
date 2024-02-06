from rest_framework import serializers

from applicants_app.serializers.applicant_serializers import ApplicantSerializer, ApplicantForJobOpeningsListSerializer
from job_openings_app.models import JobOpening


class JobOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = '__all__'


class JobOpeningListSerializer(serializers.ModelSerializer):
    job_type = serializers.CharField(source='job_type.name')
    job_category = serializers.CharField(source='job_category.name')
    job_activity = serializers.CharField(source='job_activity.name')

    employer_name = serializers.CharField(source='employer.name')
    employer_description = serializers.CharField(source='employer.description')
    employer_address = serializers.CharField(source='employer.legal_address')
    employer_site = serializers.CharField(source='employer.site')

    applicants = ApplicantForJobOpeningsListSerializer(many=True, read_only=True)

    class Meta:
        model = JobOpening
        fields = ('id', 'job_type', 'job_category', 'job_activity', 'title', 'description',
                  'salary_min', 'salary_max', 'employer_name', 'employer_description', 'employer_address',
                  'employer_site', 'created_at', 'applicants')


class JobOpeningCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = ('job_type', 'job_category', 'job_activity', 'title', 'salary_min', 'salary_max', 'description',
                  'employer')
        extra_kwargs = {
            'salary_min': {
                'style': {'placeholder': '₽'},
                'help_text': 'Заполните одно поле или укажите диапазон заработной платы. Оставьте поля '
                             'пустыми, если оплата не предполагается'
            },
            'salary_max': {
                'style': {'placeholder': '₽', }
            },
            'employer': {'required': False, 'allow_null': True},
        }


class JobOpeningListFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = ('job_type', 'job_category', 'job_activity', 'employer', 'applicants', 'archived', 'employee_found')
