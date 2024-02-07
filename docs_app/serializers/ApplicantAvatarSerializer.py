from rest_framework import serializers

from docs_app.models import ApplicantAvatar


class ApplicantRetrieveAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantAvatar
        fields = ('id', 'file', 'original_name', 'upload_time', 'extension')


class ApplicantCreateOrUpdateAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicantAvatar
        fields = ('id', 'file', 'original_name', 'extension')
