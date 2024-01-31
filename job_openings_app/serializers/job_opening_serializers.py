from rest_framework import serializers

from job_openings_app.models import JobOpening


class JobOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = '__all__'


class JobOpeningListSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source='employer.name')

    class Meta:
        model = JobOpening
        fields = ('id', 'job_type', 'job_category', 'job_activity', 'title', 'description', 'salary_min', 'salary_max',
                  'employer_name', 'created_at', 'applicants')


class JobOpeningCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = ('job_type', 'job_category', 'job_activity', 'title', 'salary_min', 'salary_max', 'description',
                  'employer')
        extra_kwargs = {
            'salary_min': {
                'style': {'placeholder': '₽',
                          'help_text': 'Заполните одно поле или укажите диапазон заработной платы. Оставьте поля '
                                       'пустыми, если оплата не предполагается'}
            },
            'salary_max': {
                'style': {'placeholder': '₽', }
            }
        }


class JobOpeningFoundApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = ('id', 'employee_found',)


class JobOpeningMoveToArchiveSerializer(serializers.Serializer):
    class Meta:
        fields = ('id', 'archived',)


class JobOpeningListFilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobOpening
        fields = ('id', 'job_type', 'job_category', 'job_activity', 'title', 'description', 'salary_min', 'salary_max',
                  'employer', 'created_at', 'applicants', 'archived', 'employee_found')
