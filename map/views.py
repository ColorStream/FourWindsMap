from django.shortcuts import render
from .models import Markers
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, permissions, viewsets
from .serializers import MarkersSerializer
import requests

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import TemplateHTMLRenderer

# Create your views here.

#https://www.django-rest-framework.org/topics/html-and-forms/

def home(request):
    
    return render(request, 'base.html')

class MarkersCreate(generics.ListCreateAPIView):
    """
    API endpoint that allows markers to be viewed.
    """
    queryset = Markers.objects.all() #.order_by('-date_posted')
    serializer_class = MarkersSerializer
    permission_classes = [permissions.AllowAny]

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