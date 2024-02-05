from django.db import models

from applicants_app.models import Applicant
from feed_app.models import Event, Excursion


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Событие')
    file = models.FileField(verbose_name='Файл')
    original_name = models.CharField(max_length=255, verbose_name='Оригинальное имя')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='Время загрузки')
    extension = models.CharField(max_length=10, verbose_name='Расширение')
    is_preview = models.BooleanField(default=False, verbose_name='Превью')

    def __str__(self):
        return f'{self.original_name} ({self.event})'

    class Meta:
        verbose_name = 'Фотография события'
        verbose_name_plural = 'Фотографии событий'
        app_label = 'docs_app'


class ExcursionImage(models.Model):
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, verbose_name='Экскурсия')
    file = models.FileField(upload_to='excursion_photos/', verbose_name='Файл')
    original_name = models.CharField(max_length=255, verbose_name='Оригинальное имя')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='Время загрузки')
    extension = models.CharField(max_length=10, verbose_name='Расширение')
    is_preview = models.BooleanField(default=False, verbose_name='Превью')

    def __str__(self):
        return f'{self.original_name} ({self.excursion})'

    class Meta:
        verbose_name = 'Фотография экскурсии'
        verbose_name_plural = 'Фотографии экскурсий'
        app_label = 'docs_app'


class ApplicantAvatar(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, verbose_name='Соискатель')
    file = models.FileField(upload_to='avatars/', verbose_name='Файл')
    original_name = models.CharField(max_length=255, verbose_name='Оригинальное имя')
    upload_time = models.DateTimeField(auto_now_add=True, verbose_name='Время загрузки')
    extension = models.CharField(max_length=10, verbose_name='Расширение')

    def __str__(self):
        return f'{self.original_name} ({self.applicant})'

    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'
        app_label = 'docs_app'
