from rest_framework import serializers
from rest_framework.serializers import FileField
from .models import Markers, Verification

class MarkersListSerializer(serializers.ListSerializer): #this goes first in order to be initialized before the main serializer
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        marker_mapping = {marker.id: marker for marker in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for marker_id, data in data_mapping.items():
            marker = marker_mapping.get(marker_id, None)
            if marker is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(marker, data))

        # Perform deletions.
        for marker_id, marker in marker_mapping.items():
            if marker_id not in data_mapping:
                marker.delete()

        return ret


class MarkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markers
        latitude = serializers.FloatField(write_only=True)
        longitude = serializers.FloatField(write_only=True)
        geojson_data = serializers.JSONField() 
        id = serializers.IntegerField()
        list_serializer_class = MarkersListSerializer
        fields = ['id', 'latitude','longitude', 'fromyear', 'storytext', 'date_posted', 'geojson_data', 'approved']
        read_only_fields = ['id', 'geojson_data', 'date_posted'] #in order for it to be readonly and still visible, it HAS to be duplicated :(

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
                #no date posted, since I think that's more relevant to moderation
                "approved": validated_data.get('approved'),
            }
        }

        # Ensure the geojson_data is included in the validated_data before creating the object
        validated_data['geojson_data'] = geojson_data

        # Now create and return the Markers instance
        marker = Markers.objects.create(**validated_data)

        # Debug print to verify GeoJSON construction (Optional)
        #print(f"GeoJSON data: {geojson_data}")

        return marker
    
    def update(self, instance, validated_data): #works using the MarkersRetrieveUpdateDestroy Update Mixin
        # update the 'approved' field from validated_data, or keep the current value
        instance.approved = validated_data.get('approved', instance.approved)
        instance.geojson_data['properties']['approved'] = instance.approved
        
        # save changes
        instance.save()

        # return marker object
        return instance
    

class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        upload = FileField()
        fields = ['upload','a1', 'a2', 'a3']
        # in case... https://stackoverflow.com/questions/35522768/django-serializer-imagefield-to-get-full-url




#geojson_data = serialize('geojson', Markers.objects.all(), geometry_field='coordinates', fields=('name',))