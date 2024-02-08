from django.contrib import admin
from .models import JobType, JobCategory, JobActivity, JobOpening, Municipality


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(JobActivity)
class JobActivityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'job_type', 'job_category', 'job_activity', 'employer', 'created_at', 'archived', 'employee_found')
    search_fields = ('title', 'description', 'employer__name', 'employer__legal_address')
    list_filter = ('job_type', 'job_category', 'job_activity', 'archived', 'employee_found')
    date_hierarchy = 'created_at'


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)