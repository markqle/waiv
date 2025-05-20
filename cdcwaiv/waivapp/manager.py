from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from waivapp.models import WaivUser, StudentPersonalInfo, StudentLog, CaseStatusInfo, StudentAcademicLog, StudentDoc, WaivServiceInfo,CounselingLog, MonthlyClientListingLog
import pandas as pd
from django.db.models import Q
from django.db import transaction

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
    case_status = CaseStatusInfo.objects.all()
    return render(request, "manager_template/add_student_template.html", {
        "case_managers": case_managers,
        "counselors":    counselors,
        "case_status": case_status,
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
        academic_plan = request.POST.get('academic_plan')
        academic_level = request.POST.get('academic_level')
        gpa = request.POST.get('gpa')
        case_manager_id = request.POST.get('case_manager') or None
        dedicated_staff_id = request.POST.get('dedicated_staff') or None
        cs_code = request.POST.get('case_status')
        if cs_code:
            status = CaseStatusInfo.objects.get(pk=cs_code)
        DOC_CODES = ['waivreferral', 'dr260', 'dr215', 'dr222', 'casenote']
        try:
            student=StudentPersonalInfo.objects.create(csulb_id=csulb_id, participant_id=participant_id, first_name=first_name, last_name=last_name, email=email, birthdate=dob, phone=phone, employ_goal=employ_goal, city=city, enrollment_date=enroll_date, intake_status=intake_status, disability_type=disability_type, disability_detail= disability_detail, case_manager_id=case_manager_id, dedicated_staff_id=dedicated_staff_id)
            StudentLog.objects.create(csulb_id=student, case_status_code=status)
            StudentAcademicLog.objects.create(csulb_id_id=student.csulb_id,academic_plan=academic_plan, academic_level=academic_level, gpa=gpa)
            for code in DOC_CODES:
                # HTML checkboxes submit the string 'on' when checked, else nothing
                if request.POST.get(f'checkbox_{code}') == 'on':
                    received = request.POST.get(f'received_{code}') or None
                    expiry   = request.POST.get(f'expiry_{code}')   or None

                    # create new row, or update existing one if it’s already there
                    StudentDoc.objects.update_or_create(
                        csulb_id_id=student.csulb_id,
                        doc_name     = code,
                        defaults={
                            'received_date': received,
                            'expiry_date':   expiry,
                        }
                    )
            messages.success(request, "Successfully Added new student")
            return HttpResponseRedirect("/add_student")
        except Exception as e:
            messages.error(request, f"Failed to Add new student: {e}")
            return HttpResponseRedirect("/add_student")
        
def add_counseling(request):
    students = StudentPersonalInfo.objects.all()
    counselors = WaivUser.objects.filter(position__in=['counselor', 'case_manager'])
    service_types = WaivServiceInfo.objects.all()
    return render(request,"manager_template/add_counseling_template.html",{
        "students": students,
        "staff_list": counselors,
        "service_types": service_types
        })

def add_counseling_save(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed", status=405)
    else:
        csulb_id = request.POST.get('student_id')
        staff_id = request.POST.get('staff_id') or None
        date_checkin = request.POST.get('datecheckin')
        case_note = request.POST.get('case_note')
        service_type_id = request.POST.get('service_type')
        try:
            CounselingLog.objects.create(
                csulb_id_id=csulb_id,
                staff_id=staff_id,
                date_checkin = date_checkin,
                case_note = case_note,
                service_type_id = service_type_id
            )
            messages.success(request, "Successfully Added new counseling note")
            return HttpResponseRedirect("/add_counseling")
        except Exception as e:
            messages.error(request, f"Failed to Add new counseling note: {e}")
            return HttpResponseRedirect("/add_counseling")


def import_monthly_client_listing(request):
    if request.method == 'POST':
        f = request.FILES['file']
        # force strings so we can detect empty cells
        if f.name.lower().endswith('.csv'):
            df = pd.read_csv(f, dtype=str)
        else:
            df = pd.read_excel(f, dtype=str)

        for _, row in df.iterrows():
            # safe extraction helper
            def get_str(col):
                val = row.get(col)
                return val.strip() if isinstance(val, str) else ''

            pid         = get_str('Participant_ID')
            status_code = get_str('Case_Status')
            counselor   = get_str('Staff_Name')
            district    = get_str('Dist')

            # lookup foreign key
            case_status = None
            if status_code:
                case_status = CaseStatusInfo.objects.filter(
                    case_description=status_code
                ).first()
            # safe date parser
            def parse_date(col):
                val = row.get(col)
                # if Pandas saw a date, it may already be a Timestamp
                if pd.isna(val) or val == '':
                    return None
                try:
                    return pd.to_datetime(val).date()
                except Exception:
                    return None

            fund_begin = parse_date('Case_Contract_Fund_Source_Start_Date')
            fund_end   = parse_date('Case_Contract_Fund_Source_End_Date')
            closure    = parse_date('Closure_Date')

            MonthlyClientListingLog.objects.update_or_create(
                participant_id=pid,
                defaults={
                    'case_status_code': case_status,
                    'dor_counselor':    counselor,
                    'fund_begin_date':  fund_begin,
                    'fund_end_date':    fund_end,
                    'closure_date':     closure,
                    'district':         district,
                }
            )

        messages.success(request, "Imported monthly client listing log successfully.")
        return redirect('import_monthly_client_listing')

    return render(request, 'manager_template/import_monthly_client_log.html')

def monthly_client_listing(request):
    logs = MonthlyClientListingLog.objects.all().order_by('-updated_date')
    ud = request.GET.get('updated_date')
    if ud:
        logs = logs.filter(updated_date=ud)
    return render(request,
                  'manager_template/monthly_client_listing.html',
                  {'logs': logs})

def manage_staff(request):
    staffs = WaivUser.objects.filter(position__in=['counselor', 'case_manager'])
    return render(request, 'manager_template/manage_staff_template.html', 
                  {"staffs": staffs})

def view_counseling(request):
    # 1) Grab the raw search text
    search = request.GET.get('search', '').strip()
    start_date  = request.GET.get('start_date', '').strip()
    end_date    = request.GET.get('end_date', '').strip()
    # 2) Build a queryset of students to populate the dropdown
    students_qs = StudentPersonalInfo.objects.all()
    if search:
        students_qs = students_qs.filter(
            Q(csulb_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    # 3) If the user has selected a student, fetch their logs
    selected_csulb = request.GET.get('student_id')
    student = None
    logs = None
    if selected_csulb:
        student = get_object_or_404(StudentPersonalInfo, csulb_id=selected_csulb)
        logs = (
            CounselingLog.objects
            .filter(csulb_id=student)
            .select_related('service_type', 'staff')
            .order_by('-date_checkin')
        )
        # 4) Apply date‐range filtering if provided
        if start_date:
            logs = logs.filter(date_checkin__gte=start_date)
        if end_date:
            logs = logs.filter(date_checkin__lte=end_date)

        logs = logs.select_related('service_type', 'staff') \
                   .order_by('-date_checkin')

    return render(request, "manager_template/view_counseling_template.html", {
        'students':    students_qs,
        'search':      search,
        'student':     student,
        'logs':        logs,
        'start_date':  start_date,
        'end_date':    end_date,
    })

def manage_student(request):
    search = request.GET.get('table_search', '').strip()
    # Use select_related to pull in the one-to-one StudentAcademicLog
    qs = StudentPersonalInfo.objects.select_related('academic_log', 'case_manager', 'dedicated_staff')


    if search:
        qs = qs.filter(
            Q(csulb_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )

    return render(request,
                  'manager_template/manage_student_template.html',
                  {
                    'students': qs,
                    'search':   search,
                  })

def edit_staff(request, staff_id):
    staff=WaivUser.objects.get(id=staff_id)
    return render(request, "manager_template/edit_staff_template.html", {"staff":staff})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        position = request.POST.get("position")
        try:
            user=WaivUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email = email
            user.username=username
            user.position = position
            user.save()
            messages.success(request, "Successfully Edit staff")
            return HttpResponseRedirect("/edit_staff/"+staff_id)
        except Exception as e:
            messages.error(request, f"Failed to edit staff: {e}")
            return HttpResponseRedirect("/edit_staff/"+staff_id)
        

# List your doc types once so you can loop over them in both views
DOC_TYPES = [
    "waivreferral",
    "dr260",
    "dr215",
    "dr222",
    "casenote",
]

def edit_student(request, csulb_id):
    """
    GET: fetch the student and related info, render the form.
    """
    student = get_object_or_404(StudentPersonalInfo, csulb_id=csulb_id)
    case_managers = WaivUser.objects.filter(position="case_manager")
    counselors    = WaivUser.objects.filter(position="counselor")
    case_statuses = CaseStatusInfo.objects.all()

    # One-to-one academic log (might not exist yet)
    try:
        academic_log = student.academic_log
    except StudentAcademicLog.DoesNotExist:
        academic_log = None

     # map existing docs by name
    existing_docs = { d.doc_name: d for d in StudentDoc.objects.filter(csulb_id=student) }

    # build a list of {"type": ..., "doc": model instance or None}
    doc_items = []
    for dt in DOC_TYPES:
        doc_items.append({
            "type": dt,
            "doc": existing_docs.get(dt)  # None if not present
        })
    academic_levels = ["Freshman", "Sophomore", "Junior", "Senior", "Master", "Graduated"]
    return render(request, "manager_template/edit_student_template.html", {
        "student":       student,
        "academic_log":  academic_log,
        "case_managers": case_managers,
        "counselors":    counselors,
        "case_statuses": case_statuses,
        "existing_docs": existing_docs,
        "DOC_TYPES":     DOC_TYPES,
        "DOC_ITEMS":      doc_items, 
        "academic_levels": academic_levels,
    })


def edit_student_save(request, csulb_id):
    """
    POST: validate & save all fields, then redirect back to edit_student.
    """
    if request.method != "POST":
        return redirect("edit_student", csulb_id=csulb_id)

    student = get_object_or_404(StudentPersonalInfo, csulb_id=csulb_id)

    with transaction.atomic():
        # --- 1) Update StudentPersonalInfo fields ---
        student.participant_id     = request.POST.get("participant_id", "")
        student.first_name         = request.POST.get("first_name", "")
        student.last_name          = request.POST.get("last_name", "")
        student.birthdate          = request.POST.get("dob")  or None
        student.email              = request.POST.get("email", "")
        student.phone              = request.POST.get("phone", "")
        student.city               = request.POST.get("city", "")
        student.enrollment_date    = request.POST.get("enroll_date") or None
        student.intake_status      = bool(int(request.POST.get("intake_status", 0)))
        student.employ_goal        = request.POST.get("employ_goal", "")
        student.disability_type    = request.POST.get("disability_type") or None
        student.disability_detail  = request.POST.get("disability_detail", "")
        student.case_manager_id    = request.POST.get("case_manager") or None
        student.dedicated_staff_id = request.POST.get("dedicated_staff") or None
        student.case_status_code_id= request.POST.get("case_status") or None
        student.save()

        # --- 2) Update or create AcademicLog ---
        al, _ = StudentAcademicLog.objects.get_or_create(csulb_id=student)
        al.academic_plan  = request.POST.get("academic_plan", "")
        al.academic_level = request.POST.get("academic_level", "")
        al.gpa            = request.POST.get("gpa") or None
        al.save()

        # --- 3) Handle each StudentDoc type ---
        for doc_type in DOC_TYPES:
            checked = request.POST.get(f"checkbox_{doc_type}") == "on"
            rec_date = request.POST.get(f"received_{doc_type}") or None
            exp_date = request.POST.get(f"expiry_{doc_type}") or None

            if checked:
                # create or update
                StudentDoc.objects.update_or_create(
                    csulb_id=student,
                    doc_name=doc_type,
                    defaults={
                        "received_date": rec_date,
                        "expiry_date":   exp_date,
                    }
                )
            else:
                # remove if it exists
                StudentDoc.objects.filter(
                    csulb_id=student,
                    doc_name=doc_type
                ).delete()

    messages.success(request, "Student record updated successfully.")
    return redirect("edit_student", csulb_id=student.csulb_id)