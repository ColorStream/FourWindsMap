from rest_framework import serializers
from .models import Markers

class MarkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markers
        fields = ['latitude', 'longitude', 'fromyear', 'storytext', 'date_posted', 'approved']