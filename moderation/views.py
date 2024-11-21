from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from map.models import Markers, Verification
from map.serializers import MarkersSerializer, VerificationSerializer


#Rest Framework Imports
from rest_framework import status, generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

# Create your views here.

#@api_view(['GET', 'POST', 'PUT', 'DELETE'])
class ModerationPanel(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = 'moderation.html'
    
    def get(self, request):
        queryset = Markers.objects.all()
        return Response({'markers': queryset})

    def post(self, request):
        queryset = Markers.objects.all()
        if request.method == 'POST':
            serializer = MarkersSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return redirect('moderation-panel')
            else:
                serializer = MarkersSerializer()  # Initialize the serializer for GET requests
        return render(request, 'moderation.html', {'markers': queryset})
    
    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = MarkersSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update()
            return redirect('moderation-panel')
        return render(request, 'moderation.html', {'markers': Markers.objects.all()})
    

    

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
def markerupdate(request, pk):
    """
    Reskin of the snippets example code. 
    """
    try:
        marker = Markers.objects.get(pk=pk)
    except Markers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        marker = Markers.objects.get(pk=pk)
        serializer = MarkersSerializer(marker)
        return Response(serializer.data)
    
    if request.method == "POST" and request.POST.get('_method') == "PUT":
        marker = get_object_or_404(Markers, pk=pk)
        data = request.data

        if 'approved' in data:
            marker.approved = data['approved']
            print(data['approved'])

            geojson_data = marker.geojson_data
            geojson_data['properties']['approved'] = data['approved']
            marker.geojson_data = geojson_data
        marker.save()
        return Response({"message": f"Marker {marker.pk} updated successfully!"}, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = MarkersSerializer(marker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        marker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'POST':
        serializer = MarkersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"