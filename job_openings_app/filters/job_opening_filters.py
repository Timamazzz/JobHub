from django_filters import rest_framework as filters
from job_openings_app.models import JobOpening
from django_filters.filters import Filter
from django.forms.fields import MultipleChoiceField, IntegerField


class MultipleValueField(MultipleChoiceField):
    def __init__(self, *args, field_class, **kwargs):
        self.inner_field = field_class()
        super().__init__(*args, **kwargs)

    def valid_value(self, value):
        return self.inner_field.validate(value)

    def clean(self, values):
        return values and [self.inner_field.clean(value) for value in values]


class MultipleValueFilter(Filter):
    field_class = MultipleValueField

    def __init__(self, *args, field_class, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, field_class=field_class, **kwargs)


class JobOpeningFilter(filters.FilterSet):
    job_activity = MultipleValueFilter(field_class=IntegerField)
    job_category = MultipleValueFilter(field_class=IntegerField)

    class Meta:
        model = JobOpening
        fields = {
            'employer': ['exact'],
            'applicants': ['exact'],
            'job_type': ['exact'],
            'archived': ['exact'],
            'employee_found': ['exact'],
        }
