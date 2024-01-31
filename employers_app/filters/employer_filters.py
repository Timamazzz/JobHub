from django_filters import rest_framework as filters
from employers_app.models import Employer


class EmployerFilter(filters.FilterSet):
    class Meta:
        model = Employer
        fields = {
            'user': ['exact'],
        }
