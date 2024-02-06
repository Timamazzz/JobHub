from rest_framework import serializers
from job_openings_app.models import JobCategory


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'


class JobCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'
