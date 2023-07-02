from django.contrib import admin
from django.urls import path, include
from project_api import urls as project_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(project_urls)),
]
