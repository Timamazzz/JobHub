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
        # Получаем полный URL-адрес файла
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None

    class Meta:
        model = ApplicantAvatar
        fields = ('id', 'file', 'original_name', 'extension')

