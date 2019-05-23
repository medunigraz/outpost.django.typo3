from django.contrib import admin

from . import models


@admin.register(models.DjangoSource)
class DjangoSourceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'private',
    )
