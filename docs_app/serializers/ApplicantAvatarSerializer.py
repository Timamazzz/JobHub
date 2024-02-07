from rest_framework import serializers

from docs_app.models import ApplicantAvatar


class ApplicantRetrieveAvatarSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = ApplicantAvatar
        fields = ('id', 'file', 'original_name', 'upload_time', 'extension')

    def get_file(self, obj):
        return obj.file.url


class ApplicantCreateOrUpdateAvatarSerializer(serializers.ModelSerializer):
    file = serializers.CharField(max_length=256)

    class Meta:
        model = ApplicantAvatar
        fields = ('id', 'file', 'original_name', 'extension')

    def update(self, instance, validated_data):
        print('update')
        instance.file = validated_data.get('file', instance.file)
        instance.original_name = validated_data.get('original_name', instance.original_name)
        instance.extension = validated_data.get('extension', instance.extension)
        instance.save()
        return instance
