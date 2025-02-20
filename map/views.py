from django.shortcuts import render
from .models import Markers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#Rest Framework Imports 
from rest_framework import generics, permissions, status, mixins
from rest_framework.parsers import JSONParser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import MarkersSerializer, VerificationSerializer
from rest_framework.views import APIView # for the map

# Create your views here.

#https://www.django-rest-framework.org/topics/html-and-forms/
class Map(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer] #JSONRenderer processes post request
    permission_classes = [AllowAny]
    template_name = 'base.html'
    
    def get(self, request):
        queryset = Markers.objects.filter(approved=True)
        return Response({'markers': queryset})

    def post(self, request):
        queryset = Markers.objects.all()
        if request.method == 'POST':
            requestdata = request.data
            verifserializer = VerificationSerializer(data=requestdata)
            if verifserializer.is_valid():
                verification = verifserializer.save()
                markerserializer = MarkersSerializer(data=requestdata)
                if markerserializer.is_valid():
                    marker = markerserializer.save()
                    marker.verification = verification #have to add it after model creation because it won't pass in validated data
                    marker.save()
                    return Response({"success": "Marker created successfully!"}, status=status.HTTP_201_CREATED)
            else:
                return Response(verifserializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'base.html', {'markers': queryset})

    

class MarkersCreate(generics.ListCreateAPIView):
    """
    API endpoint that allows markers to be viewed and posted to by authenticated moderators.
    """
    queryset = Markers.objects.all()
    serializer_class = MarkersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = MarkersSerializer(data=request.data)
        #no verification serializer on this view assuming that you're authenticated as a moderator already
        
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Marker created successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MarkersRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin): #marker-update-view
    queryset = Markers.objects.all()
    serializer_class = MarkersSerializer
    permission_class = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def patch(self, request, *args, **kwargs):
        """Does a partial update on the markers using its given serializer update() method.

        Args:
            request (HttpRequest): The request given from the marker-create-view controller.

        Returns:
            self.update(): Uses the serializer's update method to update the approval status.
        """
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        try:
            marker = self.get_object()
            if marker.verification:
                marker.verification.delete()
            return self.destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def markers_list(request):
    """
    Handles JSON responses.
    """
    if request.method == 'GET':
        markers = Markers.objects.all()
        serializer = MarkersSerializer(markers, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MarkersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)