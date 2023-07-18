from django.contrib import admin
from .models import Task


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'auto_id', 'name', 'priority',
                    'creator', 'updater', 'created_at', 'modified_at', 'is_deleted',)
    ordering = ('-created_at',)
    list_display_links = ('name',)
    filter_horizontal = ()
    list_filter = ('is_deleted',)
    fieldsets = ()


admin.site.register(Task, TaskAdmin)
