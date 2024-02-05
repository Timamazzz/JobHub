from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from JobHub.utils.ModelViewSet import ModelViewSet
from applicants_app.filters.ApplicantFilter import ApplicantFilter
from applicants_app.models import Applicant
from applicants_app.serializers.applicant_serializers import ApplicantSerializer, ApplicantRetrieveSerializer, \
    ApplicantUpdateSerializer


# Create your views here.
class ApplicantViewSet(ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_class = ApplicantFilter
    filter_backends = [DjangoFilterBackend]
    serializer_list = {
        'retrieve': ApplicantRetrieveSerializer,
        'update': ApplicantUpdateSerializer,
    }
