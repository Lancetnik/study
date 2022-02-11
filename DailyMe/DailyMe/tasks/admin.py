from django.contrib import admin

from .models import Task, TaskToDo, PeriodicTask


admin.site.register(Task)
admin.site.register(TaskToDo)
admin.site.register(PeriodicTask)
