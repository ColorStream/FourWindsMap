from django.shortcuts import render
from .models import Markers
from django.http import HttpResponse
from rest_framework import generics, permissions, viewsets
from .serializers import MarkersSerializer

# Create your views here.

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

 
