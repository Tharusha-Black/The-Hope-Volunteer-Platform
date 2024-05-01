# serializers.py

from rest_framework import serializers
from volunteer_oppertunities.models import VolantProjects

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolantProjects
        fields = '__all__'
