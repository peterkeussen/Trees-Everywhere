from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('tree.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
