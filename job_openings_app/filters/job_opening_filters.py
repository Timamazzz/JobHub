import django_filters
from django_filters import rest_framework as filters
from job_openings_app.models import JobOpening


class JobOpeningFilter(filters.FilterSet):
    job_activity = django_filters.CharFilter(field_name='job_activity__id', lookup_expr='in')
    job_category = django_filters.CharFilter(field_name='job_category__id', lookup_expr='in')

    class Meta:
        model = JobOpening
        fields = {
            'employer': ['exact'],
            'applicants': ['exact'],
            'job_type': ['exact'],
            'archived': ['exact'],
            'employee_found': ['exact'],
            'job_activity': ['in'],
            'job_category': ['in'],
        }
