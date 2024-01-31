from django_filters import rest_framework as filters
from job_openings_app.models import JobOpening


class JobOpeningFilter(filters.FilterSet):
    class Meta:
        model = JobOpening
        fields = {
            'employer': ['exact'],
            'applicants': ['exact'],
            'job_type': ['exact'],
            'job_category': ['exact'],
            'job_activity': ['exact'],
            'archived': ['exact'],
            'employee_found': ['exact'],
        }