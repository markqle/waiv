from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('profile', index),
    path('employee', index),
    path('student', index),
    path('login', index),
    path('monthly-listing', index),
    path('counseling', index),
]
