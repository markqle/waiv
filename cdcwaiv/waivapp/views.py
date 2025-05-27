from django.shortcuts           import render, redirect
from django.contrib.auth        import login, logout
from django.contrib             import messages
from django.http                import HttpResponse, HttpResponseRedirect
from waivapp.EmailBackEnd       import EmailBackEnd
from django.urls                import reverse

def showDemoPage(request):
    return render(request, "demo.html")

def showLoginPage(request):
    return render(request, "login_page.html")

def doLogin(request):
    # Only accept POST from the login form
    if request.method != "POST":
        return redirect('show_login')

    email    = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()

    # Use your custom backend to authenticate by email
    user = EmailBackEnd.authenticate(request, username=email, password=password)
    if user is None:
        messages.error(request, "Invalid email or password.")
        return redirect('show_login')

    if not user.is_active:
        messages.error(request, "Your account is inactive.")
        return redirect('show_login')

    # Everything looks good—log them in
    login(request, user)

    # Now redirect based on their role
    if user.is_superuser or user.is_staff or user.position == 'case_manager':
        return redirect('admin_home')
    elif user.position == 'counselor':
        return redirect('staff_home')
    else:
        # Fallback for any other or missing position
        logout(request)
        messages.error(request, "Your account has no valid role.")
        return redirect('show_login')
    
def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User:"+request.user.email+" position: "+request.user.position)
    else:
        return HttpResponse("Please login first")
    
def logout_user(request):
    logout(request)
    return redirect('show_login')
