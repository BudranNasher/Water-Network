from rest_framework import serializers

from .models import Valve, Tree

class ValveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valve
        fields = ['id', 'lat', 'long']

    def __str__(self):
        return self.id


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ['id', 'lat', 'long']

    def __str__(self):
        return self.id
