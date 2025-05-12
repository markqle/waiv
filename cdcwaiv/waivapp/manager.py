from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from waivapp.models import WaivUser, StudentPersonalInfo
def admin_home(request):
    return render(request, "manager_template/home_content.html")

def add_staff(request):
    return render(request,"manager_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed")
    else:
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        position=request.POST.get('position')
        try:
            user=WaivUser.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name, position=position)
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect("/add_staff")
        
def add_student(request):
    # Fetch only case managers and counselors
    case_managers = WaivUser.objects.filter(position="case_manager")
    counselors   = WaivUser.objects.filter(position="counselor")

    return render(request, "manager_template/add_student_template.html", {
        "case_managers": case_managers,
        "counselors":    counselors,
    })

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed", status=405)
    else:
        csulb_id = request.POST.get('csulb_id')
        participant_id = request.POST.get('participant_id')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        dob=request.POST.get('dob')
        phone=request.POST.get('phone')
        employ_goal = request.POST.get('employ_goal')
        city=request.POST.get('city')
        enroll_date = request.POST.get('enroll_date')
        intake_status = request.POST.get('intake_status') == "1"
        disability_type = request.POST.get('disability_type')
        disability_detail = request.POST.get('disability_detail')
        case_manager_id = request.POST.get('case_manager') or None
        dedicated_staff_id = request.POST.get('dedicated_staff') or None
        try:
            StudentPersonalInfo.objects.create(csulb_id=csulb_id, participant_id=participant_id, first_name=first_name, last_name=last_name, email=email, birthdate=dob, phone=phone, employ_goal=employ_goal, city=city, enrollment_date=enroll_date, intake_status=intake_status, disability_type=disability_type, disability_detail= disability_detail, case_manager_id=case_manager_id, dedicated_staff_id=dedicated_staff_id)
            messages.success(request, "Successfully Added new student")
            return HttpResponseRedirect("/add_student")
        except:
            messages.error(request, "Failed to Add new student")
            return HttpResponseRedirect("/add_student")
