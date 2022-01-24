from django.contrib import admin

from .models import Task, RegularTask, TaskCategory


admin.site.register(Task)
admin.site.register(TaskCategory)
admin.site.register(RegularTask)
