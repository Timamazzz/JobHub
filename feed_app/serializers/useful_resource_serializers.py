from rest_framework import serializers
from feed_app.models import UsefulResource


class UsefulResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsefulResource
        fields = '__all__'


class UsefulResourceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsefulResource
        fields = '__all__'


