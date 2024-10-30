from django.shortcuts import render
from .models import Markers
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, permissions, viewsets
from .serializers import MarkersSerializer

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

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

class MarkersRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Markers.objects.all()
    serializer_class = MarkersSerializer
    #permission_class = [permissions.IsAuthenticated]
    lookup_field = "pk"

@csrf_exempt
def markers_list(request):
    """
    Reskin of the snippet example code. 
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
 
