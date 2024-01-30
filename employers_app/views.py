from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from post_office import mail
from JobHub import settings
from JobHub.utils.ModelViewSet import ModelViewSet
from employers_app.models import Employer
from employers_app.serializers.employers_serializers import EmployerSerializer, EmployerModerationDataSerializer, \
    EmployerLoginSerializer


# Create your views here.
class EmployerViewSet(ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    serializer_list = {
        'send-to-moderation': EmployerModerationDataSerializer,
        'login': EmployerLoginSerializer,
    }

    @action(detail=False, methods=['post'], url_path='send-to-moderation')
    def send_to_moderation(self, request):
        serializer = EmployerModerationDataSerializer(data=request.data)
        if serializer.is_valid():

            subject = 'Data for Moderation'
            message = f'Data for moderation has been received:\n\n{serializer.data}'
            html_message = f'<p>Data for moderation has been received:</p><pre>{serializer.data}</pre>'

            mail.send(
                'timama.feik@mail.ru',
                settings.DEFAULT_FROM_EMAIL,
                subject=subject,
                message=message,
                html_message=html_message,
                priority='now'
            )

            return Response({'detail': 'Data sent for moderation'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

