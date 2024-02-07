from rest_framework import serializers

from docs_app.models import ApplicantAvatar


class ApplicantRetrieveAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicantAvatar
        fields = ('id', 'file', 'original_name', 'upload_time', 'extension')


class ApplicantCreateOrUpdateAvatarSerializer(serializers.ModelSerializer):
    #file = serializers.CharField(max_length=1024)
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        if obj.file:
            file_url = obj.file.url
            # Получаем путь после 'media/'
            file_path = file_url.split('media/', 1)[-1]
            return file_path
        return None

    class Meta:
        model = ApplicantAvatar
        fields = ('id', 'file', 'original_name', 'extension')

