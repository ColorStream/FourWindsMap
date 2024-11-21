from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('moderation/', views.ModerationPanel.as_view(), name='moderation-panel'),
]