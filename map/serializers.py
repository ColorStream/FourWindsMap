from rest_framework import serializers
#from rest_framework.serializers import FileField
from .models import Markers, Verification
from rest_framework.validators import UniqueTogetherValidator

class VerificationSerializer(serializers.ModelSerializer):    
    #marking all as required=False in order to make it so the custom validator works 
    upload = serializers.FileField(max_length=50, allow_empty_file=False, required=False) #max_length caps filename
    a1 = serializers.CharField(required=False)
    a2 = serializers.CharField(required=False)
    a3 = serializers.CharField(required=False)

    class Meta:
        model = Verification
        fields = ['upload', 'a1', 'a2', 'a3']
    
    def validate(self, data):
        """
        Validation to check whether the upload data is fulfilled OR the answer data is fulfilled.
        """
        upload = data.get('upload')
        a1 = data.get('a1')
        a2 = data.get('a2')
        a3 = data.get('a3')

        if upload and (a2 or a3): #Might remove
            raise serializers.ValidationError(
                "Provide either a file for or answers for the validation questions, but not both."
            )

        if not upload and not (a1 and a2 and a3): #this is to make sure someone has done at least one of the verification options
            raise serializers.ValidationError(
                "You must provide either a file in 'upload' or answers."
            )

        return data
    
    def create(self, validated_data):
        return Verification.objects.create(**validated_data)


class MarkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markers
        latitude = serializers.FloatField(write_only=True)
        longitude = serializers.FloatField(write_only=True)
        geojson_data = serializers.JSONField() 
        id = serializers.IntegerField()
        verification = serializers.PrimaryKeyRelatedField(queryset=Verification.objects.all())
        fields = ['id', 'latitude','longitude', 'fromyear', 'storytext', 'date_posted', 'geojson_data', 'approved', 'verification']
        read_only_fields = ['id', 'geojson_data', 'date_posted', 'verification'] #in order for it to be readonly and still visible, it HAS to be duplicated :(
        validators = [
            UniqueTogetherValidator(
                queryset=Markers.objects.all(),
                fields=['fromyear', 'storytext']
            )
        ]

    def create(self, validated_data):
        # manually create longitude and latitude
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

        validated_data['geojson_data'] = geojson_data

        # create and return the Markers instance
        marker = Markers.objects.create(**validated_data)

        # debug print
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
    
