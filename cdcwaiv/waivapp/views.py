from django.shortcuts import render, redirect
from django.contrib.auth    import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from waivapp.EmailBackEnd import EmailBackEnd
from rest_framework import generics
from .models import StudentPersonalInfo, WaivUser

def showDemoPage(request):
    return render(request, "demo.html")

def showLoginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method is not allowed</h2>")
    else:
        user=EmailBackEnd.authenticate(request, username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            return HttpResponseRedirect("/admin_home")
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User:"+request.user.email+" position: "+request.user.position)
    else:
        return HttpResponse("Please login first")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

