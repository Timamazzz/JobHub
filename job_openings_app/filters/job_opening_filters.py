from django_filters import rest_framework as filters

from JobHub.utils.filters import MultipleValueFilter
from job_openings_app.models import JobOpening
from django.forms.fields import IntegerField


class JobOpeningFilter(filters.FilterSet):
    job_activity = MultipleValueFilter(field_class=IntegerField)
    job_category = MultipleValueFilter(field_class=IntegerField)

    class Meta:
        model = JobOpening
        fields = {
            'employer': ['exact'],
            'applicants': ['exact'],
            'job_type': ['exact'],
            'municipality': ['exact'],
            'archived': ['exact'],
            'employee_found': ['exact'],
        }
