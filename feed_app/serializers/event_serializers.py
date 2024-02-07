from rest_framework import serializers

from docs_app.models import EventImage
from feed_app.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventListSerializer(serializers.ModelSerializer):
    preview_image = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_preview_image(self, event):
        preview_image = EventImage.objects.filter(event=event, is_preview=True).first()
        if preview_image:
            preview_image.replace("media/", "")
        return preview_image.file.url if preview_image else None


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        exclude = ['event', 'id', 'is_preview']


class EventRetrieveSerializer(serializers.ModelSerializer):
    gallery = serializers.SerializerMethodField()
    preview_image = serializers.SerializerMethodField()

    class Meta:
        model = Event
        exclude = ['id']

    def get_gallery(self, obj):
        images = EventImage.objects.filter(event=obj, is_preview=False)
        return ImageSerializer(images, many=True).data

    def get_preview_image(self, event):
        preview_image = EventImage.objects.filter(event=event, is_preview=True).first()
        if preview_image:
            preview_image.replace("media/", "")
        return preview_image.file.url if preview_image else None