from rest_framework import serializers
from JobHub.utils.fields import PhoneField
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
