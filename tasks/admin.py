from django.contrib import admin
from tasks.models import Task, TaskSet, Stalker, Active


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'task_set', 'public', 'type']
    search_fields = ['id', 'title', 'text', 'example_solution']
    list_filter = ['type', 'public', 'task_set']

admin.site.register(Task, TaskAdmin)


class TaskSetAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'public']
    search_fields = ['id', 'title']
    list_filter = ['public']

admin.site.register(TaskSet, TaskSetAdmin)


class ActiveAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'task_set']
    search_fields = ['user__username', 'task__id', 'task_set__id']
    list_filter = ['task_set']

admin.site.register(Active, ActiveAdmin)


class StalkerAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'seen']
    search_fields = ['task__id', 'task__task_set__id', 'user__username']
    list_filter = ['task__task_set']

admin.site.register(Stalker, StalkerAdmin)
