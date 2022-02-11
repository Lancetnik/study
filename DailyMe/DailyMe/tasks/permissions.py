
class OnlyOwnerMixin:
    def get_queryset(self):
        owner = self.request.user
        tasks = self.queryset.filter(owner=owner)
        return tasks


class OnlyToDoOwnerMixin:
    def get_queryset(self):
        owner = self.request.user
        tasks = self.queryset.prefetch_related('task').filter(task__owner=owner)
        return tasks
