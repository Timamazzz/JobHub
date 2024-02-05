from JobHub.utils.ModelViewSet import ModelViewSet
from applicants_app.models import Applicant
from applicants_app.serializers.applicant_serializers import ApplicantSerializer, ApplicantRetrieveSerializer, \
    ApplicantUpdateSerializer


# Create your views here.
class ApplicantViewSet(ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    serializer_list = {
        'retrieve': ApplicantRetrieveSerializer,
        'update': ApplicantUpdateSerializer,
    }
