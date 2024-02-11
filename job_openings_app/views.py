from django_filters.rest_framework import DjangoFilterBackend
from post_office import mail
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from JobHub import settings
from JobHub.utils.ModelViewSet import ModelViewSet
from employers_app.models import Employer
from job_openings_app.filters.job_opening_filters import JobOpeningFilter
from job_openings_app.models import JobOpening, JobCategory, JobActivity, Municipality
from job_openings_app.pagination import CustomPagination
from job_openings_app.serializers.job_activity_serializers import JobActivitySerializer, JobActivityListSerializer
from job_openings_app.serializers.job_category_serializers import JobCategorySerializer, JobCategoryListSerializer
from job_openings_app.serializers.job_opening_serializers import JobOpeningSerializer, JobOpeningListSerializer, \
    JobOpeningCreateUpdateSerializer, JobOpeningListFilterSerializer, WorkOnHolidayDataSerializer
from users_app.permissions import IsEmployer, IsApplicant, IsApplicantVerify
from rest_framework.decorators import permission_classes as action_permission_classes


# Create your views here.
class JobOpeningViewSet(ModelViewSet):
    queryset = JobOpening.objects.all().order_by('-created_at')
    serializer_class = JobOpeningSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly | IsApplicantVerify | IsEmployer]
    pagination_class = CustomPagination
    pagination_class.page_size = 6
    filterset_class = JobOpeningFilter
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description', 'job_type__name', 'job_category__name', 'job_activity__name',
                     'employer__name', 'employer__legal_address']

    serializer_list = {
        'list': JobOpeningListSerializer,
        'create': JobOpeningCreateUpdateSerializer,
        'update': JobOpeningCreateUpdateSerializer,
        'filter-list': JobOpeningListFilterSerializer,
        'work-on-holiday': WorkOnHolidayDataSerializer
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

    @action(detail=True, methods=['post'])
    def respond(self, request, *args, **kwargs):
        job_opening = self.get_object()

        user = request.user
        applicant = user.applicant_profile

        if not user.applicant_profile.is_profile_complete():
            return Response({"message": "Заполните все данные профиля"}, status=status.HTTP_403_FORBIDDEN)

        if job_opening.applicants.filter(id=applicant.id).exists():
            return Response({"message": "Вы уже откликнулись на эту вакансию."}, status=status.HTTP_400_BAD_REQUEST)

        subject = f'На вашу вакансию поступил отклик (rabota.belregion.ru)'
        message = (
            f'{job_opening.title}\n'
            f'Имя: {applicant.fio}\n'
            f'Дата рождения: {applicant.birth_date}\n'
            f'Телефон: {applicant.phone_number}\n'
            f'Email: {applicant.email}\n'
            f'Резюме: {applicant.resume}\n'
            'Это письмо отправлено автоматически. Пожалуйста, не отвечайте на него.\n\n'
            'УВЕДОМЛЕНИЕ О КОНФИДЕНЦИАЛЬНОСТИ: Это электронное сообщение и любые документы, приложенные к нему, содержат конфиденциальную информацию. Настоящим уведомляем Вас о том, что если это сообщение не предназначено Вам, использование, копирование, распространение информации, содержащейся в настоящем сообщении, а также осуществление любых действий на основе этой информации, строго запрещено. Если Вы получили это сообщение по ошибке, пожалуйста, сообщите об этом отправителю по электронной почте и удалите это сообщение.'
        )
        html_message = (
            f'<p><strong>{job_opening.title}</strong></p>'
            f'<p><strong>Имя:</strong> {applicant.fio}</p>'
            f'<p><strong>Дата рождения:</strong> {applicant.birth_date}</p>'
            f'<p><strong>Телефон:</strong> {applicant.phone_number}</p>'
            f'<p><strong>Email:</strong> {applicant.email}</p>'
            f'<p><strong>Резюме:</strong> {applicant.resume}</p>'
            '<p><br></p>'
            '<p>Это письмо отправлено автоматически. Пожалуйста, не отвечайте на него.</p>'
            '<p><br></p>'
            '<p><strong>УВЕДОМЛЕНИЕ О КОНФИДЕНЦИАЛЬНОСТИ:</strong> Это электронное сообщение и любые документы, приложенные к нему, содержат конфиденциальную информацию. Настоящим уведомляем Вас о том, что если это сообщение не предназначено Вам, использование, копирование, распространение информации, содержащейся в настоящем сообщении, а также осуществление любых действий на основе этой информации, строго запрещено. Если Вы получили это сообщение по ошибке, пожалуйста, сообщите об этом отправителю по электронной почте и удалите это сообщение.</p>'
        )

        mail.send(
            ['89205731783@mail.ru', 'job.ump@belregion.ru',  job_opening.employer.email],
            settings.DEFAULT_FROM_EMAIL,
            subject=subject,
            message=message,
            html_message=html_message,
            priority='now'
        )

        job_opening.applicants.add(applicant)
        job_opening.save()

        return Response({"message": "Вы успешно откликнулись на эту вакансию."}, status=status.HTTP_200_OK)


class JobCategoryViewSet(ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None
    serializer_list = {
        'list': JobCategoryListSerializer,
    }


class JobActivityViewSet(ModelViewSet):
    queryset = JobActivity.objects.all()
    serializer_class = JobActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None
    serializer_list = {
        'list': JobActivityListSerializer,
    }


class WorkOnHolidayAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = WorkOnHolidayDataSerializer(data=request.data)
        if serializer.is_valid():
            subject = 'Заявка работа на каникулах (rabota.belregion.ru)'
            message = (
                f'Соискатель:\n'
                f'{serializer.data.get("fio")}\n'
                f'{serializer.data.get("phone_number")}\n'
                f'{serializer.data.get("email")}\n'
                f'{serializer.data.get("municipality")}\n\n'
                'Это письмо отправлено автоматически. Пожалуйста, не отвечайте на него.\n\n'
                'УВЕДОМЛЕНИЕ О КОНФИДЕНЦИАЛЬНОСТИ: Это электронное сообщение и любые документы, приложенные к нему, содержат конфиденциальную информацию. Настоящим уведомляем Вас о том, что если это сообщение не предназначено Вам, использование, копирование, распространение информации, содержащейся в настоящем сообщении, а также осуществление любых действий на основе этой информации, строго запрещено. Если Вы получили это сообщение по ошибке, пожалуйста, сообщите об этом отправителю по электронной почте и удалите это сообщение.'
            )
            html_message = (
                f'<p><strong>Соискатель:</strong></p>'
                f'<p>{serializer.data.get("fio")}</p>'
                f'<p>{serializer.data.get("phone_number")}</p>'
                f'<p>{serializer.data.get("email")}</p>'
                f'<p>{Municipality.objects.get(id=serializer.data.get("municipality"))}</p>'
                '<p><br></p>'
                '<p>Это письмо отправлено автоматически. Пожалуйста, не отвечайте на него.</p>'
                '<p><br></p>'
                '<p><strong>УВЕДОМЛЕНИЕ О КОНФИДЕНЦИАЛЬНОСТИ:</strong> Это электронное сообщение и любые документы, приложенные к нему, содержат конфиденциальную информацию. Настоящим уведомляем Вас о том, что если это сообщение не предназначено Вам, использование, копирование, распространение информации, содержащейся в настоящем сообщении, а также осуществление любых действий на основе этой информации, строго запрещено. Если Вы получили это сообщение по ошибке, пожалуйста, сообщите об этом отправителю по электронной почте и удалите это сообщение.</p>'
            )

            mail.send(
                ['89205731783@mail.ru', 's.soprov@yandex.ru', 'job.ump@belregion.ru'],
                settings.DEFAULT_FROM_EMAIL,
                subject=subject,
                message=message,
                html_message=html_message,
                priority='now'
            )

            return Response({'detail': 'Data sent'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid data', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
