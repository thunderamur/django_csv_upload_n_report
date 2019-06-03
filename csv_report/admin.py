from django.contrib import admin

from .models import WorkTime


@admin.register(WorkTime)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'hours')
