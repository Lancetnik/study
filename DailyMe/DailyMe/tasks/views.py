from rest_framework import viewsets

from . import models, serializers
from .permissions import OnlyOwnerMixin, OnlyToDoOwnerMixin


class TaskViewSet(OnlyOwnerMixin, viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer


class ToDoViewSet(OnlyToDoOwnerMixin, viewsets.ModelViewSet):
    queryset = models.TaskToDo.objects.all()
    serializer_class = serializers.ToDoSerializer
