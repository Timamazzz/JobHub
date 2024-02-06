from rest_framework import serializers

from docs_app.models import ApplicantAvatar


class ApplicantRetrieveAvatarSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = ApplicantAvatar
        fields = ('file', 'original_name', 'upload_time', 'extension')

    def get_file(self, obj):
        return obj.file.url


class ApplicantCreateAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicantAvatar
        fields = ('id', 'file', 'original_name', 'extension')
