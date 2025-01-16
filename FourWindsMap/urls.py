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
import map.views as map_views
from django.conf import settings
from django.conf.urls.static import  static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', map_views.Map.as_view(), name='map'),
    path('map-api/', include('map.urls')),
    path('modpanel/', include('moderation.urls')),
    path('api-auth/', include('rest_framework.urls')), #for a browsable API
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
