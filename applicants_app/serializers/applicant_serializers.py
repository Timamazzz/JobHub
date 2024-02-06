import traceback

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from JobHub.utils.fields import PhoneField
from applicants_app.models import Applicant
from docs_app.models import ApplicantAvatar
from docs_app.serializers.ApplicantAvatarSerializer import ApplicantCreateAvatarSerializer, \
    ApplicantRetrieveAvatarSerializer


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantRetrieveSerializer(serializers.ModelSerializer):
    avatar = ApplicantRetrieveAvatarSerializer()

    class Meta:
        model = Applicant
        fields = ('id', 'avatar', 'fio', 'birth_date', 'phone_number', 'email', 'resume')


class ApplicantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantUpdateSerializer(serializers.ModelSerializer):
    avatar = ApplicantCreateAvatarSerializer(required=False)
    phone_number = PhoneField()

    def create(self, validated_data):
        avatar_data = validated_data.pop('avatar', None)  # Получаем данные о аватаре, если они есть
        applicant = super().create(validated_data)  # Создаем аппликанта

        if avatar_data:  # Если данные о аватаре есть
            ApplicantAvatar.objects.create(applicant=applicant, **avatar_data)  # Создаем новый аватар

        return applicant

    def update(self, instance, validated_data):
        avatar_data = validated_data.pop('avatar', None)  # Получаем данные о аватаре, если они есть
        if avatar_data:  # Если данные о аватаре есть
            avatar_instance = instance.avatar  # Получаем существующий аватар, если он есть
            if avatar_instance:  # Если аватар существует, обновляем его
                avatar_serializer = ApplicantCreateAvatarSerializer(instance=avatar_instance, data=avatar_data)
                if avatar_serializer.is_valid():
                    avatar_serializer.save()
            else:  # Если аватар не существует, создаем новый
                ApplicantAvatar.objects.create(applicant=instance, **avatar_data)

        return super().update(instance, validated_data)

    class Meta:
        model = Applicant
        fields = ('avatar', 'fio', 'birth_date', 'phone_number', 'email', 'resume')


class ApplicantForJobOpeningsListSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Applicant
        fields = ('id', 'avatar_url')

    def get_avatar_url(self, obj):
        try:
            return obj.avatar.file.url
        except AttributeError:
            return None