from rest_framework import serializers

from .models import Valve, Tree


class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ['id', 'lat', 'long']


class ValveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tree
        fields = ['id', 'lat', 'long']


#for returning trees assigned to each valve
class ValveSerializer_2(serializers.ModelSerializer):
    valves = TreeSerializer(many=True)

    class Meta:
        model = Valve
        fields = ['id', 'lat', 'long', 'valves']
