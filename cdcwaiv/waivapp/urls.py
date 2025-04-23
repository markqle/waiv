from django.urls import path, include
from .views import main

urlpatterns = [
    path('', main)
]