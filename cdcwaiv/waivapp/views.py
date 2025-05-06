from django.shortcuts import render, redirect
from django.contrib.auth    import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from waivapp.EmailBackEnd import EmailBackEnd
from rest_framework import generics
from .forms import StudentDocForm

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

def upload_doc(request):
    if request.method == "POST":
        form = StudentDocForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success_url")
    else:
        form = StudentDocForm()
    return render(request, "upload_doc.html", {"form": form})
