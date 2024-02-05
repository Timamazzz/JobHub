from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
        'get-by-user': ApplicantRetrieveSerializer,
    }

    @action(detail=False, methods=['GET'], url_path='get-by-user')
    def get_by_user(self, request):
        user = request.user
        queryset = Applicant.objects.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
