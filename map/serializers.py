from rest_framework import serializers
#from rest_framework_gis.serializers import GeoFeatureModelSerializer
#from django.core.serializers import serialize
from .models import Markers

class MarkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markers
        latitude = serializers.FloatField(write_only=True)
        longitude = serializers.FloatField(write_only=True)
        geojson_data = serializers.JSONField(write_only=True) 
        #geo_field = 'point'
        fields = ['latitude','longitude', 'fromyear', 'storytext', 'date_posted', 'geojson_data', 'approved']
        read_only_fields = ['geojson_data'] #in order for it to be readonly and still visible, it HAS to be duplicated :(

    def create(self, validated_data):
        # Construct GeoJSON from the latitude and longitude
        geojson_data = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [validated_data['longitude'], validated_data['latitude']],
            },
            "properties": {
                "fromyear": validated_data.get('fromyear'),
                "storytext": validated_data.get('storytext'),
                "date_posted": validated_data.get('date_posted'),
                # Add approved if needed
                # "approved": validated_data.get('approved'),
            }
        }

        # Ensure the geojson_data is included in the validated_data before creating the object
        validated_data['geojson_data'] = geojson_data

        # Now create and return the Markers instance
        marker = Markers.objects.create(**validated_data)

        # Debug print to verify GeoJSON construction (Optional)
        print(f"GeoJSON data: {geojson_data}")

        return marker





#geojson_data = serialize('geojson', Markers.objects.all(), geometry_field='coordinates', fields=('name',))