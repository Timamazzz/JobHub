from django.contrib import admin
from .models import Applicant
from django.http import HttpResponse
import openpyxl

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('user', 'fio', 'birth_date', 'phone_number', 'email', 'vk_id')
    search_fields = ('user__username', 'fio', 'phone_number', 'email', 'vk_id')
    list_filter = ('birth_date',)
    actions = ['export_to_excel']

    def export_to_excel(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Соискатели"

        headers = ['ID', 'ФИО', 'Дата рождения', 'Номер телефона', 'Email', 'Резюме', 'ID ВКонтакте']
        ws.append(headers)

        for applicant in queryset:
            row = [
                applicant.id,
                applicant.fio,
                applicant.birth_date,
                applicant.phone_number,
                applicant.email,
                applicant.resume,
                applicant.vk_id
            ]
            ws.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=applicants.xlsx'
        wb.save(response)
        return response

    export_to_excel.short_description = "Экспорт в Excel"

admin.site.register(Applicant, ApplicantAdmin)
