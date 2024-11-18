"""
URL configuration for FourWindsMap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    #path('', views.Map.as_view(), name='map'),
    path('markers/', views.MarkersCreate.as_view(), name="marker-create-view"),
    path('markers/manage/<int:pk>', views.MarkersRetrieveUpdateDestroy.as_view(), name="marker-update-view"),
    path('markerslist', views.markers_list, name='markerslist'),
    path('moderation/', views.moderation, name='moderation-panel'),
]
