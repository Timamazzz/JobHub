from rest_framework import serializers
from JobHub.utils.fields import PhoneField, PasswordField
from employers_app.models import Employer


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'


class EmployerModerationDataSerializer(serializers.ModelSerializer):
    phone_number = PhoneField()

    class Meta:
        model = Employer
        fields = ('name', 'inn', 'legal_address', 'contact_person_fio', 'phone_number')


class EmployerLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, label='Логин', )
    password = PasswordField(label='Пароль',
                             help_text='Восстановление пароля',
                             style={'tip_message': 'Здесь какая то подскзка, но я ее не знаю'}, )

    class Meta:
        model = Employer
        fields = ('username', 'password')


class EmployerFilterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ('user',)
