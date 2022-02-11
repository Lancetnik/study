from django.urls import path

from . import views


urlpatterns = [
    path('', views.TaskViewSet.as_view({"get": "list"})),
    path('<int:pk>/', views.TaskViewSet.as_view({"get": "retrieve"})),
    path('create/', views.TaskViewSet.as_view({"post": "create"})),
    path('delete/<int:pk>/', views.TaskViewSet.as_view({"delete": "destroy"})),

    path('todo/', views.ToDoViewSet.as_view({"get": "list"})),
    path('todo/<int:pk>/', views.ToDoViewSet.as_view({"get": "retrieve"})),
    path('todo/create/', views.ToDoViewSet.as_view({"post": "create"})),
    path('todo/delete/<int:pk>/', views.ToDoViewSet.as_view({"delete": "destroy"})),
]
