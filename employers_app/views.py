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
            subject = 'Регистрация нового работодателя (rabota.belregion.ru)'
            message = (
                f'Наименование: {serializer.validated_data.get("name")}\n'
                f'ИНН: {serializer.validated_data.get("inn")}\n'
                f'Ул {serializer.validated_data.get("legal_address")}\n'
                f'{serializer.validated_data.get("contact_person_fio")}\n'
                f'{serializer.validated_data.get("phone_number")}\n'
                f'{serializer.validated_data.get("contact_person_email")}\n'
                'Это письмо отправлено автоматически. Пожалуйста, не отвечайте на него.\n\n'
                'УВЕДОМЛЕНИЕ О КОНФИДЕНЦИАЛЬНОСТИ: Это электронное сообщение и любые документы, приложенные к нему, содержат конфиденциальную информацию. Настоящим уведомляем Вас о том, что если это сообщение не предназначено Вам, использование, копирование, распространение информации, содержащейся в настоящем сообщении, а также осуществление любых действий на основе этой информации, строго запрещено. Если Вы получили это сообщение по ошибке, пожалуйста, сообщите об этом отправителю по электронной почте и удалите это сообщение.'
            )
            html_message = (
                f'<p><strong>Наименование:</strong> {serializer.validated_data.get("name")}</p>'
                f'<p><strong>ИНН:</strong> {serializer.validated_data.get("inn")}</p>'
                f'<p><strong>Ул {serializer.validated_data.get("legal_address")}</strong></p>'
                f'<p>{serializer.validated_data.get("contact_person_fio")}</p>'
                f'<p>{serializer.validated_data.get("phone_number")}</p>'
                f'<p>{serializer.validated_data.get("contact_person_email")}</p>'
                '<p><br></p>'
                '<p>Это письмо отправлено автоматически. Пожалуйста, не отвечайте на него.</p>'
                '<p><br></p>'
                '<p><strong>УВЕДОМЛЕНИЕ О КОНФИДЕНЦИАЛЬНОСТИ:</strong> Это электронное сообщение и любые документы, приложенные к нему, содержат конфиденциальную информацию. Настоящим уведомляем Вас о том, что если это сообщение не предназначено Вам, использование, копирование, распространение информации, содержащейся в настоящем сообщении, а также осуществление любых действий на основе этой информации, строго запрещено. Если Вы получили это сообщение по ошибке, пожалуйста, сообщите об этом отправителю по электронной почте и удалите это сообщение.</p>'
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
