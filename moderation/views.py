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

class ModerationPanel(APIView): #TODO add some sort of indication it's been toggled
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = 'moderation.html'
    
    def get(self, request):
        markers = Markers.objects.all().order_by('-date_posted')
        verification = Verification.objects.all()
        for marker in markers:
            print(marker.verification)
        return Response({'markers': markers, 'verification': verification})

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
    
    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

   

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"