from django.shortcuts import render

# Create your views here.
def index(request, *arg, **kwargs):
    return render(request, "frontend/index.html")