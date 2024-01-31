from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from JobHub.utils.ModelViewSet import ModelViewSet
from employers_app.models import Employer
from job_openings_app.filters.job_opening_filters import JobOpeningFilter
from job_openings_app.models import JobOpening
from job_openings_app.serializers.job_opening_serializers import JobOpeningSerializer, JobOpeningListSerializer, \
    JobOpeningCreateUpdateSerializer, JobOpeningListFilterSerializer


# Create your views here.
class JobOpeningViewSet(ModelViewSet):
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer
    filterset_class = JobOpeningFilter
    serializer_list = {
        'list': JobOpeningListSerializer,
        'create': JobOpeningCreateUpdateSerializer,
        'update': JobOpeningCreateUpdateSerializer,
        'filter-list': JobOpeningListFilterSerializer,
    }

    def perform_create(self, serializer):
        try:
            employer = Employer.objects.get(user=self.request.user)
        except Employer.DoesNotExist:
            raise ValidationError("User does not have associated Employer")

        if employer:
            serializer.save(employer=employer)
        else:
            raise ValidationError("User does not have associated Employer")

    def perform_update(self, serializer):
        try:
            employer = Employer.objects.get(user=self.request.user)
        except Employer.DoesNotExist:
            raise ValidationError("User does not have associated Employer")

        if employer:
            serializer.save(employer=employer)
        else:
            raise ValidationError("User does not have associated Employer")

    @action(detail=True, methods=['post'], url_path='found-applicants')
    def found_applicants(self, request, pk=None):
        job_opening = self.get_object()
        job_opening.archived = True
        job_opening.employee_found = True
        job_opening.save()

        return Response({'detail': 'Applicants found for the job opening.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='move-to-archive')
    def move_to_archive(self, request, pk=None):
        job_opening = self.get_object()
        job_opening.archived = True
        job_opening.save()

        return Response({'detail': 'Job opening moved to archive.'}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        query = request.query_params.get('query', '')

        if query:
            queryset = queryset.filter(
                job_type__name__icontains=query,
                job_category__name__icontains=query,
                job_activity__name__icontains=query,
                title__icontains=query,
                description__icontains=query,
                employer__name__icontains=query,
                employer__legal_address__icontains=query
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
