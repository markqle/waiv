from django.shortcuts import render, redirect
from django.contrib.auth    import authenticate, login
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
        user=EmailBackEnd.authenticate(request, request.POST.get("email"),request.POST.get("password"))
        if user!=None:
            login(request,user)
            return HttpResponse("Email: "+request.POST.get("email")+" Password: "+request.POST.get("password"))
        else:
            return HttpResponse("Invalid Login")

def upload_doc(request):
    if request.method == "POST":
        form = StudentDocForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success_url")
    else:
        form = StudentDocForm()
    return render(request, "upload_doc.html", {"form": form})
