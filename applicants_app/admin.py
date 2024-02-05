from django.contrib import admin
from .models import Applicant


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('user', 'fio', 'birth_date', 'phone_number', 'email', 'vk_id')
    search_fields = ('user__username', 'fio', 'phone_number', 'email', 'vk_id')
    list_filter = ('birth_date',)


admin.site.register(Applicant, ApplicantAdmin)
