from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from JobHub.utils.ModelViewSet import ModelViewSet
from job_openings_app.models import JobOpening
from job_openings_app.serializers.job_opening_serializers import JobOpeningSerializer, JobOpeningListSerializer, \
    JobOpeningCreateUpdateSerializer, JobOpeningFoundApplicantSerializer, JobOpeningMoveToArchiveSerializer


# Create your views here.
class JobOpeningViewSet(ModelViewSet):
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer
    serializer_list = {
        'list': JobOpeningListSerializer,
        'create': JobOpeningCreateUpdateSerializer,
        'update': JobOpeningCreateUpdateSerializer,
        'found-applicants': JobOpeningFoundApplicantSerializer,
        'move-to-archive': JobOpeningMoveToArchiveSerializer,
    }

    @action(detail=True, methods=['post'], url_path='found-applicants')
    def found_applicants(self, request, pk=None):
        job_opening = self.get_object()
        serializer = JobOpeningFoundApplicantSerializer(instance=job_opening, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Applicants found for the job opening.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='move-to-archive')
    def move_to_archive(self, request, pk=None):
        job_opening = self.get_object()
        serializer = JobOpeningMoveToArchiveSerializer(instance=job_opening, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Job opening moved to archive.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)