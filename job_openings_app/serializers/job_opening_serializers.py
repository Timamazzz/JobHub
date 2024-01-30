from rest_framework import serializers

from job_openings_app.models import JobOpening


class JobOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = '__all__'


class JobOpeningListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = ('id', 'job_type', 'job_category', 'job_activity', 'title')


class JobOpeningCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpening
        fields = ()
