from rest_framework import viewsets
from JobHub.utils.OptionsMetadata import OptionsMetadata
from JobHub.utils.UpdateModelMixin import UpdateModelMixin


class ModelViewSet(viewsets.ModelViewSet, UpdateModelMixin):
    serializer_list = {}
    metadata_class = OptionsMetadata

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_list.get(self.action, self.serializer_class)
