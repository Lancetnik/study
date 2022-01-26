from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('task/', include('tasks.urls')),

    path('my-admin-page/', admin.site.urls),
]
