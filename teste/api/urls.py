from django.urls import path
from .views import PlantTreeAPIView

urlpatterns = [
    path('', PlantTreeAPIView.as_view(), name='api_listtree')
]