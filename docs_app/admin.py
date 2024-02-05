from django.contrib import admin
from docs_app.models import *


#
#
# @admin.register(EventImage)
# class PhotoEventAdmin(admin.ModelAdmin):
#     list_display = ('original_name', 'event', 'upload_time', 'is_preview')
#     search_fields = ('original_name', 'event__text')
#
#
# @admin.register(ExcursionImage)
# class PhotoExcursionAdmin(admin.ModelAdmin):
#     list_display = ('original_name', 'excursion', 'upload_time', 'is_preview')
#     search_fields = ('original_name', 'excursion__text')

@admin.register(ApplicantAvatar)
class ApplicantAvatarAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'applicant', 'upload_time')
    search_fields = ('original_name', )
