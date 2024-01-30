from rest_framework import serializers

from feed_app.models import Event
from users_app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
