from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок', null=True, blank=True)
    publish_time = models.DateTimeField(verbose_name='Время публикации события', default=timezone.now)
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        app_label = 'feed_app'


class Excursion(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок', null=True, blank=True)
    publish_time = models.DateTimeField(verbose_name='Время публикации экскурсии', default=timezone.now)
    is_open = models.BooleanField(verbose_name='Экскурсия открыта', default=True)
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Экскурсия'
        verbose_name_plural = 'Экскурсии'
        app_label = 'feed_app'


class UsefulResource(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    link = models.URLField(verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Полезный ресурс'
        verbose_name_plural = 'Полезные ресурсы'
        app_label = 'feed_app'
