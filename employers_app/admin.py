from job_openings_app.models import JobOpening
from django.contrib import admin
from django.http import HttpResponse
import openpyxl
from .models import Employer

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn', 'legal_address', 'phone_number', 'email')
    search_fields = ('name', 'inn', 'phone_number', 'email')
    list_filter = ('name',)

    def export_to_excel(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active

        ws.append([
            'Название компании',
            'ИНН',
            'Юридический адрес',
            'Номер телефона',
            'Email',
            'Описание',
            'Сайт',
            'Название вакансии',
            'Описание вакансии',
            'Кол-во откликнувшихся соискателей'
        ])

        for employer in queryset:
            ws.append([
                employer.name,
                employer.inn,
                employer.legal_address,
                employer.phone_number,
                employer.email,
                employer.description,
                employer.site if employer.site else '',
            ])

            job_openings = JobOpening.objects.filter(employer=employer)
            for job_opening in job_openings:
                ws.append([
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    job_opening.title,
                    job_opening.description,
                    job_opening.applicants.count()
                ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=employers_data.xlsx'
        wb.save(response)
        return response

    export_to_excel.short_description = "Экспорт в Excel"

