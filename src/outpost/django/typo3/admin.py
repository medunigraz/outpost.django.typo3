from django.contrib import admin

from . import models


@admin.register(models.DjangoSource)
class DjangoSourceAdmin(admin.ModelAdmin):
    list_display = ("id", "private")


@admin.register(models.DjangoStorage)
class DjangoStorageAdmin(admin.ModelAdmin):
    list_display = ("id", "url")


class SourceLanguageInline(admin.TabularInline):
    model = models.SourceLanguage


@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "private")
    inlines = (SourceLanguageInline,)
    readonly_fields = ("id", "title", "private")

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        return
