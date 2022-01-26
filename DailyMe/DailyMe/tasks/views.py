from django.http import JsonResponse, HttpResponse

from .models import Task, TaskCategory, RegularTask


def create_task(requset):
    owner = requset.user

    if (text := requset.POST.get('text')) is None:
        return HttpResponse('`text` field is required', status=400)

    task = Task.objects.create(owner=owner, text=text)
    return JsonResponse(task.to_dict(), status=201)


def get_all_tasks(requset):
    owner = requset.user
    tasks = Task.objects.filter(owner=owner)
    return JsonResponse(
        [task.to_dict() for task in tasks],
        safe=False
    )


def get_task(requset, pk):
    owner = requset.user
    tasks = Task.objects.filter(owner=owner)
    try:
        task = tasks.get(pk=pk)
    except Task.DoesNotExist:
        return HttpResponse(status=404)
    else:
        return JsonResponse(task.to_dict(), safe=False)



from rest_framework import generics
from .serializers import TaskCreateSerializer, TaskSerializer


class TaskCreate(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer


class OnlyOnwerMixin:
    serializer_class = TaskSerializer

    def get_queryset(self):
        owner = self.request.user
        tasks = Task.objects.filter(owner=owner)
        return tasks


class TaskList(OnlyOnwerMixin, generics.ListAPIView):
    pass


class TaskRetrieve(OnlyOnwerMixin, generics.RetrieveAPIView):
    pass
