# serializers.py
from rest_framework import serializers
from docs_app.models import ExcursionImage
from feed_app.models import Excursion


class ExcursionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = '__all__'


class ExcursionListSerializer(serializers.ModelSerializer):
    preview_image = serializers.SerializerMethodField()

    class Meta:
        model = Excursion
        fields = '__all__'

    def get_preview_image(self, excursion):
        preview_image = ExcursionImage.objects.filter(excursion=excursion, is_preview=True).first()
        if preview_image:
            preview_image.replace("media/", "")
        return preview_image.file.url if preview_image else None


class ExcursionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcursionImage
        exclude = ['excursion', 'id', 'is_preview']


class ExcursionRetrieveSerializer(serializers.ModelSerializer):
    gallery = serializers.SerializerMethodField()
    preview_image = serializers.SerializerMethodField()

    class Meta:
        model = Excursion
        exclude = ['id']

    def get_gallery(self, obj):
        images = ExcursionImage.objects.filter(excursion=obj, is_preview=False)
        return ExcursionImageSerializer(images, many=True).data

    def get_preview_image(self, excursion):
        preview_image = ExcursionImage.objects.filter(excursion=excursion, is_preview=True).first()
        if preview_image:
            preview_image.replace("media/", "")
        return preview_image.file.url if preview_image else None
