from django.contrib import admin
from tasks.models import Task, TaskSet, Stalker, Active


admin.site.register(Task)
admin.site.register(TaskSet)
admin.site.register(Active)
admin.site.register(Stalker)
