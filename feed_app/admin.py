from django.contrib import admin

from docs_app.models import ExcursionImage, EventImage
from .models import Event, Excursion, UsefulResource
from django.db import models
from ckeditor.widgets import CKEditorWidget

class PhotoEventInline(admin.TabularInline):
    model = EventImage
    exclude = ['original_name', 'extension']
    extra = 1


class PhotoExcursionInline(admin.TabularInline):
    model = ExcursionImage
    exclude = ['original_name', 'extension']
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', 'text', )
    inlines = [PhotoEventInline]
    exclude = ['publish_time']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='default')}
    }


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_open', 'text')
    search_fields = ('text', 'title')
    list_filter = ('is_open',)
    inlines = [PhotoExcursionInline]
    exclude = ['publish_time']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='default')}
    }


@admin.register(UsefulResource)
class UsefulResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')
    search_fields = ('name', 'link')

