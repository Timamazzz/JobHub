from django.db import models

from applicants_app.models import Applicant
from employers_app.models import Employer


class JobType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
        app_label = 'job_openings_app'


class JobCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид'
        verbose_name_plural = 'Виды'
        app_label = 'job_openings_app'


class JobActivity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Род деятельности'
        verbose_name_plural = 'Роды деятельности'
        app_label = 'job_openings_app'


class JobOpening(models.Model):
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE, verbose_name='Тип')
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, verbose_name='Вид')
    job_activity = models.ForeignKey(JobActivity, on_delete=models.CASCADE, verbose_name='Род деятельности')
    title = models.CharField(max_length=255, verbose_name='Название вакансии')
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Зарплата от')
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Зарплата до')
    description = models.TextField(verbose_name='Описание')
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, verbose_name='Работодатель')
    applicants = models.ManyToManyField(Applicant, related_name='job_applications', blank=True, verbose_name='Откликнувшиеся')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    archived = models.BooleanField(default=False, verbose_name='Архивная')
    employee_found = models.BooleanField(default=False, verbose_name='Сотрудник найден')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        app_label = 'job_openings_app'
