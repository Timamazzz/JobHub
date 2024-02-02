"""
URL configuration for JobHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from JobHub import settings
from JobHub.utils.FileUploadView import FileUploadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users_app.urls')),
    path('api/feed/', include('feed_app.urls')),
    path('api/applicants/', include('applicants_app.urls')),
    path('api/employers/', include('employers_app.urls')),
    path('api/job-openings/', include('job_openings_app.urls')),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    path('auth/', include('rest_framework_social_oauth2.urls')),
]
