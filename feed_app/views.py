from rest_framework import permissions

from JobHub.utils.ModelViewSet import ModelViewSet
from feed_app.models import Event, Excursion, UsefulResource
from feed_app.serializers.event_serializers import EventSerializer, EventRetrieveSerializer, EventListSerializer
from feed_app.serializers.excursion_serializers import ExcursionSerializer, ExcursionListSerializer, \
    ExcursionRetrieveSerializer
from feed_app.serializers.useful_resource_serializers import UsefulResourceSerializer, UsefulResourceListSerializer


# Create your views here.
class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_list = {
        'list': EventListSerializer,
        'retrieve': EventRetrieveSerializer,
    }


class ExcursionViewSet(ModelViewSet):
    queryset = Excursion.objects.all()
    serializer_class = ExcursionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_list = {
        'list': ExcursionListSerializer,
        'retrieve': ExcursionRetrieveSerializer,
    }


class UsefulResourceViewSet(ModelViewSet):
    queryset = UsefulResource.objects.all()
    serializer_class = UsefulResourceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_list = {
        'list': UsefulResourceListSerializer,
    }
