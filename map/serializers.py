from rest_framework import serializers
#from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.core.serializers import serialize
from .models import Markers

class MarkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markers
        latitude = serializers.FloatField(write_only=True)
        longitude = serializers.FloatField(write_only=True)
        geojson_data = serializers.JSONField(read_only=True)
        #geo_field = 'point'
        fields = ['latitude', 'longitude', 'fromyear', 'storytext', 'date_posted', 'approved']

        def create(self, validated_data):
            # Construct GeoJSON from the latitude and longitude
            geojson_data = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [validated_data['longitude'], validated_data['latitude']],
                },
                "properties": {
                    "fromyear": validated_data['name'],
                    "storytext": validated_data['storytext'],
                    "date_posted": validated_data['date_posted'],
                    #"approved": validated_data['approved']
                }
            }

            # Remove the latitude and longitude from validated data since we don't want to store those separately
            validated_data.pop('latitude')
            validated_data.pop('longitude')

            # Create and save the Markers instance with GeoJSON data
            marker = Markers.objects.create(
                geojson_data=geojson_data, 
                **validated_data
            )
            return marker


#geojson_data = serialize('geojson', Markers.objects.all(), geometry_field='coordinates', fields=('name',))