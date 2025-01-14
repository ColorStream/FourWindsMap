from map.models import Markers
from django.shortcuts import render

#Rest Framework Imports
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.

class ModerationPanel(APIView): 
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = 'moderation.html'
    
    def get(self, request):
        markers = Markers.objects.all().order_by('-date_posted')
        return Response({'markers': markers})