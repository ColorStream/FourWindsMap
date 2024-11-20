from django.shortcuts import render, get_object_or_404, redirect
from .models import Markers
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt

#Rest Framework Imports 
from rest_framework import generics, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import MarkersSerializer
from rest_framework.views import APIView # for the map

# Create your views here.

#https://www.django-rest-framework.org/topics/html-and-forms/
#@api_view(['GET', 'PUT'])
class Map(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [AllowAny]
    template_name = 'base.html'

    
    def get(self, request):
        queryset = Markers.objects.all()
        return Response({'markers': queryset})

    def post(self, request):
        queryset = Markers.objects.all()
        if request.method == 'POST':
            serializer = MarkersSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return redirect('map')
            else:
                serializer = MarkersSerializer()  # Initialize the serializer for GET requests
        return render(request, 'map.html', {'markers': queryset})

class MarkersCreate(generics.ListCreateAPIView):
    """
    API endpoint that allows markers to be viewed.
    """
    queryset = Markers.objects.all() #.order_by('-date_posted')
    serializer_class = MarkersSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MarkersSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Marker created successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#so i can show in a list
from rest_framework import mixins
from rest_framework import generics

class MarkersList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Markers.objects.all()
    serializer_class = MarkersSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class MarkersRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Markers.objects.all()
    serializer_class = MarkersSerializer
    #permission_class = [permissions.IsAuthenticated]
    lookup_field = "pk"

@csrf_exempt
def markers_list(request):
    """
    Reskin of the Markers example code. 
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
 
def moderation(request):
    """Moderation panel for approving and deletings markers. 

    Args:
        request (_type_): _description_
    """
    response = requests.get('http://127.0.0.1:8000/map-api/markerslist')
    data = response.json()
    return render(request, 'moderation.html', {'data': data})