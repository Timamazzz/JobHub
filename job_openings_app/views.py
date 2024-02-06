from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.decorators import action, permission_classes as view_permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from JobHub.utils.ModelViewSet import ModelViewSet
from employers_app.models import Employer
from job_openings_app.filters.job_opening_filters import JobOpeningFilter
from job_openings_app.models import JobOpening, JobCategory, JobActivity
from job_openings_app.serializers.job_activity_serializers import JobActivitySerializer, JobActivityListSerializer
from job_openings_app.serializers.job_category_serializers import JobCategorySerializer, JobCategoryListSerializer
from job_openings_app.serializers.job_opening_serializers import JobOpeningSerializer, JobOpeningListSerializer, \
    JobOpeningCreateUpdateSerializer, JobOpeningListFilterSerializer
from users_app.permissions import IsEmployer, IsApplicant


# Create your views here.
class JobOpeningViewSet(ModelViewSet):
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = JobOpeningFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description', 'job_type__name', 'job_category__name', 'job_activity__name',
                     'employer__name', 'employer__legal_address']
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
    @permission_classes([IsEmployer])
    def found_applicants(self, request, pk=None):
        job_opening = self.get_object()
        job_opening.archived = True
        job_opening.employee_found = True
        job_opening.save()

        return Response({'detail': 'Applicants found for the job opening.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='move-to-archive')
    @view_permission_classes((IsEmployer, ))
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

    @action(detail=True, methods=['post'])
    @permission_classes([IsApplicant])
    def respond(self, request, *args, **kwargs):
        job_opening = self.get_object()
        user = request.user
        applicant = user.applicant
        job_opening.applicants.append(applicant)
        job_opening.save()
        return Response(JobOpeningListSerializer(data=job_opening).data)


class JobCategoryViewSet(ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_list = {
        'list': JobCategoryListSerializer,
    }


class JobActivityViewSet(ModelViewSet):
    queryset = JobActivity.objects.all()
    serializer_class = JobActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_list = {
        'list': JobActivityListSerializer,
    }
