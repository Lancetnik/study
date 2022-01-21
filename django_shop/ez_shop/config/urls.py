from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from product.views import index


urlpatterns = [
    path('', index),

    path('product/', include('product.urls')),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
