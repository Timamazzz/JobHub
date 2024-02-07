from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from docs_app.models import ApplicantAvatar


class ApplicantRetrieveAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantAvatar
        fields = ('id', 'file', 'original_name', 'upload_time', 'extension')


class ApplicantCreateOrUpdateAvatarSerializer(serializers.ModelSerializer):
    file = serializers.CharField()

    def to_representation(self, instance):
        if isinstance(instance, ApplicantAvatar):
            request = self.context.get('request')
            if request is not None:
                file_url = request.build_absolute_uri(instance.file.url)
            else:
                file_url = instance.file.url
            return {
                'id': instance.id,
                'file': file_url,
                'original_name': instance.original_name,
                'extension': instance.extension
            }
        return super().to_representation(instance)

    class Meta:
        model = ApplicantAvatar
        fields = ('id', 'file', 'original_name', 'extension')
