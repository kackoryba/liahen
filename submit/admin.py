from django.contrib import admin

from submit.models import Submit


class SubmitAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'message', 'language', 'timestamp']
    search_fields = ['user__username', 'task__id', 'task__task_set__id']
    list_filter = ['language', 'message']

admin.site.register(Submit, SubmitAdmin)
