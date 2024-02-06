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

    def create(self, validated_data):
        print('ApplicantCreateAvatarSerializer create')
        return ApplicantAvatar.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print('ApplicantCreateAvatarSerializer update')
        instance.file = validated_data.get('file', instance.file)
        instance.original_name = validated_data.get('original_name', instance.original_name)
        instance.extension = validated_data.get('extension', instance.extension)
        instance.save()
        return instance

