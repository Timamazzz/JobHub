from rest_framework import serializers
from JobHub.utils.fields import PhoneField, PasswordField
from employers_app.models import Employer


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'


class EmployerModerationDataSerializer(serializers.ModelSerializer):
    phone_number = PhoneField()
    contact_person_email = serializers.EmailField(required=False, label="Email контактного лица")
    contact_person_fio = serializers.CharField(max_length=255, label="ФИО контактного лица")

    class Meta:
        model = Employer
        fields = ('name', 'inn', 'legal_address', 'contact_person_fio', 'contact_person_fio', 'phone_number', 'description', 'site', 'contact_person_email')
        extra_kwargs = {
            'description' : {
                'required': True,
                'label': 'Описание организации'
            },
            'site': {
                'required': True,
                'label': 'Ссылка на сайт организации'
            },
        }


class EmployerLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, label='Логин', )
    password = PasswordField(label='Пароль',
                             help_text='Восстановление пароля',
                             style={'tip_message': "Для восстановления пароля требуется связаться с администратором "
                                                   "по электронной почте: <a href='mailto:job.ump@belregion.ru'>job.ump@belregion.ru</a> "
                                                   "и подтвердить свою личность"})

    class Meta:
        model = Employer
        fields = ('username', 'password')


class EmployerFilterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ('user',)


class EmployerRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'
