from django.contrib import admin
from .models import Employer


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn', 'legal_address', 'phone_number', 'email')
    search_fields = ('name', 'inn', 'phone_number', 'email')
    list_filter = ('name',)
