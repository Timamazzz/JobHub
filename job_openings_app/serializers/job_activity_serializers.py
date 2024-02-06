from rest_framework import serializers
from job_openings_app.models import JobActivity


class JobActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobActivity
        fields = '__all__'


class JobActivityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobActivity
        fields = '__all__'
