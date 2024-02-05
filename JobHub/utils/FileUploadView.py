from uuid import uuid4
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from datetime import datetime
import os
from urllib.parse import urlparse


class FileUploadSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False))


def save_uploaded_files(uploaded_files, path='uploads/'):
    result_data = []

    for uploaded_file in uploaded_files:
        print('uploaded_file', uploaded_file)
        if hasattr(uploaded_file, 'url') and bool(urlparse(uploaded_file.url).scheme) and uploaded_file.startswith('http'):
            url = uploaded_file.url
            original_name = os.path.basename(urlparse(url).path)
            extension = os.path.splitext(original_name)[-1].lower()
        else:
            original_name = uploaded_file.name
            extension = os.path.splitext(original_name)[-1].lower()
            new_name = f"{uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}{extension}"

            path = default_storage.save(os.path.join(path, new_name), uploaded_file)
            url = default_storage.url(path)

        file_data = {
            'url': url,
            'original_name': original_name,
            'time_upload': datetime.now(),
            'extension': extension,
        }

        result_data.append(file_data)

    return result_data


class FileUploadView(APIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        uploaded_files = request.FILES.getlist('files')
        path = request.GET.get('path', 'uploads/')

        result_data = save_uploaded_files(uploaded_files, path)

        return Response(result_data, status=status.HTTP_201_CREATED)
