from django.urls import path

from . import views


urlpatterns = [
    path('<int:pk>/', views.get_task),
    path('all/', views.get_all_tasks),
    path('create/', views.create_task),

    path('drf/create/', views.TaskCreate.as_view()),
    path('drf/all/', views.TaskList.as_view()),
    path('drf/<int:pk>/', views.TaskRetrieve.as_view()),
]
