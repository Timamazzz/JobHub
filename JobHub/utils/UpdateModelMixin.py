from rest_framework.response import Response


def FeleFieldUpdate(model, id, filename, filefield=None):
    instance = model.objects.get(id=id)
    if not filename == {}:
        if filename.startswith('/media/'):
            filename = filename.replace('/media/', '')

        instance.file.name = filename
        instance.save()
    else:
        instance.file.name = None
        instance.save()


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        print('Updating model')
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if request.data.pop('file'):

            filename = request.data.get('file', None) if not request.data.get('file') == "" else None
            request.data.pop('file', None)

            if filename or filename == {}:
                FeleFieldUpdate(serializer.Meta.model, serializer.data['id'], filename)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
