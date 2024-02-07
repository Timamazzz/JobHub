import traceback

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from JobHub.utils.fields import PhoneField
from applicants_app.models import Applicant
from docs_app.models import ApplicantAvatar
from docs_app.serializers.ApplicantAvatarSerializer import ApplicantCreateOrUpdateAvatarSerializer, \
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
    #avatar = ApplicantCreateOrUpdateAvatarSerializer(required=False)
    phone_number = PhoneField()
    avatar = serializers.DictField(child=serializers.CharField(), required=False)

    class Meta:
        model = Applicant
        fields = ('id', 'avatar', 'fio', 'birth_date', 'phone_number', 'email', 'resume')

    def create(self, validated_data):
        avatar_data = validated_data.pop('avatar', None)
        applicant = Applicant.objects.create(**validated_data)

        if avatar_data:
            avatar = ApplicantAvatar.objects.create(**avatar_data, applicant=applicant)
            applicant.avatar = avatar
            applicant.save()

        return applicant

    def update(self, instance, validated_data):
        avatar_data = validated_data.pop('avatar', None)
        if avatar_data:
            avatar_id = avatar_data.pop('id', None)
            if avatar_id:
                # Обновляем существующий аватар
                avatar = instance.avatar
                avatar.file = avatar_data.get('file', avatar.file)
                avatar.original_name = avatar_data.get('original_name', avatar.original_name)
                avatar.extension = avatar_data.get('extension', avatar.extension)
                avatar.save()
            else:
                # Создаем новый аватар
                avatar = ApplicantAvatar.objects.create(**avatar_data, applicant=instance)
                instance.avatar = avatar

        instance.fio = validated_data.get('fio', instance.fio)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.resume = validated_data.get('resume', instance.resume)
        instance.save()

        return instance


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