from rest_framework import serializers
from tree.models import PlantedTree

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantedTree
        fields = ('age', 'planted_at', 'user', 'tree', 'account', 'latitude', 'longitude')