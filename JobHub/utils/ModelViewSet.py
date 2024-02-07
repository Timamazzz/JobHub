from rest_framework import viewsets
from rest_framework.response import Response
from JobHub.utils.OptionsMetadata import OptionsMetadata


def FileFieldUpdate(model, id, filename, filefield=None):
    instance = model.objects.get(id=id)
    if not filename == {}:
        if filename.startswith('/media/'):
            filename = filename.replace('/media/', '')

        instance.file.name = filename
        instance.save()
    else:
        instance.file.name = None
        instance.save()


class ModelViewSet(viewsets.ModelViewSet):
    serializer_list = {}
    metadata_class = OptionsMetadata

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_list.get(self.action, self.serializer_class)

    def update(self, request, *args, **kwargs):
        print('Updating model')
        partial = kwargs.pop('partial', False)
        filename = None
        print('request.data', request.data)

        if request.data.pop('file'):
            filename = request.data.get('file', None) if not request.data.get('file') == "" else None
            request.data.pop('file', None)

        print('request.data', request.data)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if filename or filename == {}:
            FileFieldUpdate(serializer.Meta.model, serializer.data['id'], filename)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
