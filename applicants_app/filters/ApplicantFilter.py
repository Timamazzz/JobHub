from django_filters import rest_framework as filters

from applicants_app.models import Applicant


class ApplicantFilter(filters.FilterSet):
    class Meta:
        model = Applicant
        fields = {
            'user': ['exact'],
        }
