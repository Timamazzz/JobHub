from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from post_office import mail
from rest_framework.views import APIView

from JobHub import settings
from JobHub.utils.ModelViewSet import ModelViewSet
from employers_app.filters.employer_filters import EmployerFilter
from employers_app.models import Employer
from employers_app.serializers.employers_serializers import EmployerSerializer, EmployerModerationDataSerializer, \
    EmployerLoginSerializer, EmployerFilterListSerializer, EmployerRetrieveSerializer
from users_app.permissions import IsEmployer


# Create your views here.
class EmployerViewSet(ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    filterset_class = EmployerFilter
    permission_classes = [IsEmployer]
    serializer_list = {
        'send-to-moderation': EmployerModerationDataSerializer,
        'login': EmployerLoginSerializer,
        'filter-list': EmployerFilterListSerializer,
        'get-by-user': EmployerRetrieveSerializer
    }

    @action(detail=False, methods=['GET'], url_path='get-by-user')
    def get_by_user(self, request):
        user = request.user
        employer = user.employer_profile
        serializer = EmployerRetrieveSerializer(employer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendToModerationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmployerModerationDataSerializer(data=request.data)
        if serializer.is_valid():
            subject = 'Data for Moderation'
            message = (
                'Data for moderation has been received:\n\n'
                f'Company Name: {serializer.validated_data.get("name")}\n'
                f'INN: {serializer.validated_data.get("inn")}\n'
                f'Legal Address: {serializer.validated_data.get("legal_address")}\n'
                f'Contact Person Full Name: {serializer.validated_data.get("contact_person_fio")}\n'
                f'Phone Number: {serializer.validated_data.get("phone_number")}\n'
                f'Contact Person Email: {serializer.validated_data.get("contact_person_email")}\n'
            )
            html_message = (
                '<p>Data for moderation has been received:</p>'
                '<pre>'
                f'<strong>Company Name:</strong> {serializer.validated_data.get("name")}\n'
                f'<strong>INN:</strong> {serializer.validated_data.get("inn")}\n'
                f'<strong>Legal Address:</strong> {serializer.validated_data.get("legal_address")}\n'
                f'<strong>Contact Person Full Name:</strong> {serializer.validated_data.get("contact_person_fio")}\n'
                f'<strong>Phone Number:</strong> {serializer.validated_data.get("phone_number")}\n'
                '</pre>'
            )

            mail.send(
                ['89205731783@mail.ru', 'job.ump@belregion.ru'],
                settings.DEFAULT_FROM_EMAIL,
                subject=subject,
                message=message,
                html_message=html_message,
                priority='now'
            )

            return Response({'detail': 'Data sent for moderation'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid data', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
