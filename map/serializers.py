from rest_framework import serializers
#from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.core.serializers import serialize
from .models import Markers

class MarkersSerializer(serializers.Serializer):
    class Meta:
        model = Markers
        #geo_field = 'point'
        fields = ['latitude', 'longitude', 'fromyear', 'storytext', 'date_posted', 'approved']


#geojson_data = serialize('geojson', Markers.objects.all(), geometry_field='coordinates', fields=('name',))