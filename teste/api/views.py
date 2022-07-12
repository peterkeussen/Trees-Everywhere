from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from tree.models import PlantedTree
from .serializers import PlantSerializer

class PlantTreeAPIView(generics.ListAPIView):
    serializer_class = PlantSerializer
    renderer_classes = [JSONRenderer]
    
    def get_queryset(self):
        user = self.request.user        
        return PlantedTree.objects.filter(user=user)
    
    
    