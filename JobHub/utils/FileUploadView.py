from uuid import uuid4
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from datetime import datetime
import os


class FileUploadSerializer(serializers.Serializer):
    files = serializers.ListField( child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False))


class FileUploadView(APIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        result_data = []

        path = request.GET.get('path', 'uploads/')

        for file in files:
            original_name = file.name
            extension = os.path.splitext(original_name)[-1].lower()
            new_name = f"{uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}{extension}"

            path = default_storage.save(os.path.join(path, new_name), file)
            url = default_storage.url(path)

            extra_data = {
                'additional_info': 'value',
            }

            file_data = {
                'url': url,
                'original_name': original_name,
                'time_upload': datetime.now(),
                'extension': extension,
                **extra_data,
            }

            result_data.append(file_data)

        return Response(result_data, status=status.HTTP_201_CREATED)
