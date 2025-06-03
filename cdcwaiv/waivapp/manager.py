from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from waivapp.forms import AddStudentForm
from waivapp.models import WaivUser, StudentPersonalInfo, StudentLog, CaseStatusInfo, StudentAcademicLog, StudentDoc, WaivServiceInfo,CounselingLog, MonthlyClientListingLog, CheckinSimplicity
import pandas as pd
import string
import datetime
from datetime import timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from io import BytesIO
from django.urls import reverse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.db.models import Q, Count, F, OuterRef, Subquery
from django.db import transaction
from collections import Counter
import json

def admin_home(request):
    # define the 1-month lookback
    today      = timezone.now().date()
    last_month = today - datetime.timedelta(days=30)

    # build a list of each date in the last month
    date_list = [
        last_month + datetime.timedelta(days=i)
        for i in range((today - last_month).days + 1)
    ]
    # formatted labels for the X axis
    ts_labels = [d.strftime('%Y-%m-%d') for d in date_list]

    # 1) Case‐status changes in the last month, grouped by description (bar)
    cs_qs = (
        StudentLog.objects
        .filter(updated_date__date__gte=last_month)
        .values('case_status_code__case_description')
        .annotate(count=Count('pk'))
    )
    cs_labels = [item['case_status_code__case_description'] for item in cs_qs]
    cs_values = [item['count'] for item in cs_qs]

    # 2) Counseling sessions per day (time series)
    counseling_ts = [
        CounselingLog.objects.filter(date_checkin=d).count()
        for d in date_list
    ]

    # 3) New intakes per day (time series)
    intake_ts = [
        StudentPersonalInfo.objects.filter(
            intake_status=True,
            enrollment_date=d
        ).count()
        for d in date_list
    ]

    # 4) Sessions per Staff in last month (bar)
    staff_qs = (
        CounselingLog.objects
        .filter(date_checkin__gte=last_month)
        .values('staff__first_name', 'staff__last_name')
        .annotate(count=Count('pk'))
    )
    staff_labels = [
        f"{item['staff__first_name']} {item['staff__last_name']}"
        for item in staff_qs
    ]
    staff_values = [item['count'] for item in staff_qs]

    return render(request, "manager_template/home_content.html", {
        # bar chart data
        'cs_labels':        json.dumps(cs_labels),
        'cs_values':        json.dumps(cs_values),
        'staff_labels':     json.dumps(staff_labels),
        'staff_values':     json.dumps(staff_values),

        # time‐series line chart data
        'ts_labels':        json.dumps(ts_labels),
        'counseling_ts':    json.dumps(counseling_ts),
        'intake_ts':        json.dumps(intake_ts),
    })

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
    form = AddStudentForm()
    action_path = reverse('add_student_save')

    left_fields = [
        "csulb_id", "participant_id", "last_name", "first_name",
        "birthdate", "employ_goal", "academic_plan",
        "academic_level", "gpa", "email"
    ]
    right_fields = [
        "phone", "city", "enrollment_date", "intake_status",
        "disability_type", "disability_detail", "case_manager",
        "dedicated_counselor", "case_status"
    ]

    return render(request, "manager_template/add_student_template.html", {
        "form": form,
        "action_path": action_path,
        "button_text": "Add Student",
        "left_fields": left_fields,
        "right_fields": right_fields,
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
        birthdate      = request.POST.get('birthdate')
        phone=request.POST.get('phone')
        employ_goal = request.POST.get('employ_goal')
        city=request.POST.get('city')
        enrollment_date = request.POST.get('enrollment_date')
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
            student=StudentPersonalInfo.objects.create(csulb_id=csulb_id, participant_id=participant_id, first_name=first_name, last_name=last_name, email=email, birthdate=birthdate, phone=phone, employ_goal=employ_goal, city=city, enrollment_date=enrollment_date, intake_status=intake_status, disability_type=disability_type, disability_detail= disability_detail, case_manager_id=case_manager_id, dedicated_staff_id=dedicated_staff_id)
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
        if f.name.lower().endswith('.csv'):
            df = pd.read_csv(f, dtype=str)
        else:
            df = pd.read_excel(f, dtype=str)

        for _, row in df.iterrows():
            def get_str(col):
                v = row.get(col)
                return v.strip() if isinstance(v, str) else ''

            pid   = get_str('Participant_ID')
            raw   = get_str('Staff_Name')
            # normalize to “John Doe” rather than ALL CAPS or all lowercase
            counselor = string.capwords(raw.lower())
            status_code = get_str('Case_Status')
            district    = get_str('Dist')

            case_status = None
            if status_code:
                case_status = (
                    CaseStatusInfo.objects
                    .filter(case_description=status_code)
                    .first()
                )

            def parse_date(col):
                v = row.get(col)
                if pd.isna(v) or v == '':
                    return None
                try:
                    return pd.to_datetime(v).date()
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

def import_checkin_simplicity(request):
    """
    Upload a CSV or XLSX of Simplicity check-in data. If Event_Type is blank
    but Staff_Name is provided, fill Event_Type = "In-person counseling".
    """
    if request.method == 'POST':
        f = request.FILES.get('file')
        if not f:
            messages.error(request, "No file was uploaded.")
            return redirect('import_checkin_simplicity')

        # 1) Read into DataFrame (all columns as strings)
        if f.name.lower().endswith('.csv'):
            try:
                df = pd.read_csv(f, dtype=str)
            except Exception as e:
                messages.error(request, f"Error reading CSV: {e}")
                return redirect('import_checkin_simplicity')
        else:
            try:
                df = pd.read_excel(f, dtype=str)
            except ImportError:
                messages.error(
                    request,
                    "To import .xlsx you need openpyxl. Install via `pip install openpyxl`, or upload a CSV."
                )
                return redirect('import_checkin_simplicity')
            except Exception as e:
                messages.error(request, f"Error reading Excel: {e}")
                return redirect('import_checkin_simplicity')

        # 2) Iterate rows
        for _, row in df.iterrows():
            def get_str(col):
                v = row.get(col)
                return v.strip() if isinstance(v, str) else ''

            pid        = get_str('Student ID')   # e.g. "123456"
            raw_staff  = get_str('Counselor')       # e.g. "DOE, JOHN"
            event_type = get_str('Event Type')       # might be blank
            name       = get_str('Name')             # student’s name
            location   = get_str('Location')         # event/location

            # If Event_Type is blank but we do have a Staff_Name, assume “In-person counseling”
            if (not event_type) and raw_staff:
                event_type = "In-person counseling"

            # Parse "Date_Checkin" like "9/6/2024  12:00:00 PM"
            def parse_date(col):
                v = row.get(col)
                if pd.isna(v) or v == '':
                    return None
                try:
                    # Try exact "M/D/YYYY HH:MM:SS AM/PM" format
                    return pd.to_datetime(v, format="%m/%d/%Y %I:%M:%S %p").date()
                except Exception:
                    try:
                        return pd.to_datetime(v).date()
                    except Exception:
                        return None

            date_checkin = parse_date('Time Recorded')

            # Normalize staff name ("DOE, JOHN" → "John Doe") and attempt lookup
            counselor_name = string.capwords(raw_staff.replace(",", "").lower())
            staff_instance = None
            if counselor_name:
                parts = counselor_name.split()
                if len(parts) >= 2:
                    first, last = parts[0], " ".join(parts[1:])
                    staff_instance = WaivUser.objects.filter(
                        first_name__iexact=first,
                        last_name__iexact=last
                    ).first()

            # 3) Create/update CheckinSimplicity (no FK enforcement on csulb_id)
            CheckinSimplicity.objects.update_or_create(
                csulb_id=pid,
                date_checkin=date_checkin,
                event_type=event_type,
                defaults={
                    'staff':    staff_instance,
                    'name':     name,
                    'location': location,
                }
            )

        messages.success(request, "Imported check-in simplicity log successfully.")
        return redirect('import_checkin_simplicity')

    return render(request, 'manager_template/import_checkin_simplicity.html')

def checkin_simplicity(request):
    """
    Show all CheckinSimplicity rows, optionally filtered by imported_date.
    """
    import datetime
    # Grab a sorted list of every distinct imported_date
    distinct_dates = (
        CheckinSimplicity.objects
        .values_list('imported_date', flat=True)
        .order_by('-imported_date')
        .distinct()
    )

    ud   = request.GET.get('imported_date')
    logs = CheckinSimplicity.objects.all().order_by('-imported_date')
    if ud:
        try:
            parsed_date = datetime.datetime.strptime(ud, '%Y-%m-%d').date()
            logs = logs.filter(imported_date=parsed_date)
        except ValueError:
            pass

    return render(request, 'manager_template/checkin_simplicity.html', {
        'logs':           logs,
        'distinct_dates': distinct_dates,
        'selected_date':  ud or '',
    })

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
    last_log = (
        StudentLog.objects
        .filter(csulb_id=student)
        .order_by('-updated_date')
        .first()
    )
    current_status_code = last_log.case_status_code.case_status_code if last_log else None
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
        "current_status_code": current_status_code,
    })


def edit_student_save(request, csulb_id):
    """
    POST: validate & save all fields, then redirect back to edit_student.
    """
    if request.method != "POST":
        return redirect("edit_student", csulb_id=csulb_id)

    student = get_object_or_404(StudentPersonalInfo, csulb_id=csulb_id)
    last_log = (
        StudentLog.objects
        .filter(csulb_id=student)
        .order_by('-updated_date')
        .first()
    )
    old_status = last_log.case_status_code.case_status_code if last_log else None

    # 2) Get the new status from the form
    new_status = request.POST.get("case_status") or None
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
        student.save()
        if new_status and new_status != old_status:
            StudentLog.objects.create(
                csulb_id=student,
                case_status_code_id=new_status
            )
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

def create_monthly_report(request):
    # dropdown choices
    counselors = (
        MonthlyClientListingLog.objects
        .values_list('dor_counselor', flat=True)
        .distinct()
    )
    dates = (
        MonthlyClientListingLog.objects
        .values_list('updated_date', flat=True)
        .distinct()
    )

    selected_counselor = request.GET.get('dor_counselor')
    selected_date_str  = request.GET.get('updated_date')
    selected_date = None
    if selected_date_str:
        try:
            # try to parse "May 20, 2025" or "2025-05-20"
            selected_date = datetime.datetime.strptime(
                selected_date_str, '%B %d, %Y'
            ).date()
        except ValueError:
            try:
                selected_date = datetime.datetime.strptime(
                    selected_date_str, '%Y-%m-%d'
                ).date()
            except ValueError:
                selected_date = None

    rows = []
    if selected_counselor and selected_date:
        logs = MonthlyClientListingLog.objects.filter(
            dor_counselor=selected_counselor,
            updated_date=selected_date
        )
        for log in logs:
            try:
                student = StudentPersonalInfo.objects.get(
                    participant_id=log.participant_id
                )
            except StudentPersonalInfo.DoesNotExist:
                continue
            rows.append({
                'participant_id': log.participant_id,
                'csulb_id':       student.csulb_id,
                'name':           f"{student.first_name} {student.last_name}",
            })

    return render(request, 'manager_template/create_monthly_report.html', {
        'counselors':         counselors,
        'dates':              dates,
        'selected_counselor': selected_counselor,
        'selected_date':      selected_date,
        'rows':               rows,
    })


def monthly_report_detail(request):
    # pull in query params
    pid       = request.GET.get('participant_id')
    counselor = request.GET.get('dor_counselor')
    up_date   = request.GET.get('updated_date')
    if not pid or not counselor or not up_date:
        # You could redirect back with an error message or render a 400
        return redirect('create_monthly_report')
    
    student = get_object_or_404(
        StudentPersonalInfo,
        participant_id=pid
    )
    case_manager = student.case_manager  # WaivUser FK
    counseling_logs = (
        CounselingLog.objects
        .filter(csulb_id=student)
        .select_related('service_type', 'staff')
        .order_by('date_checkin')
    )

    # initial form data
    today = datetime.date.today().strftime("%Y-%m-%d")
    defaults = {
        'progress':    '',
        'plan':        '',
        'staff_sign':  request.user.get_full_name(),
        'staff_title': '',
        'date':        today,
    }

    # if user clicked “Export PDF”…
    if request.method == 'POST' and request.POST.get('export') == 'pdf':
        # pull each field explicitly
        progress    = request.POST.get('progress',    defaults['progress'])
        plan        = request.POST.get('plan',        defaults['plan'])
        staff_sign  = request.POST.get('staff_sign',  defaults['staff_sign'])
        staff_title = request.POST.get('staff_title', defaults['staff_title'])
        date_field  = request.POST.get('date',        defaults['date'])
        html = render_to_string('manager_template/monthly_report_pdf.html', {
            'student':         student,
            'case_manager':    case_manager,
            'dor_counselor':   counselor,
            'counseling_logs': counseling_logs,
            'progress':        progress,
            'plan':            plan,
            'staff_sign':      staff_sign,
            'staff_title':     staff_title,
            'date':            date_field,
        })
        result = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=result)
        if pisa_status.err:
            return HttpResponse('PDF generation error', status=500)
        response = HttpResponse(
            result.getvalue(),
            content_type='application/pdf'
        )
        fname = f"Monthly_Report_{student.csulb_id}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{fname}"'
        return response

    return render(request, 'manager_template/monthly_report_detail.html', {
        'student':         student,
        'case_manager':    case_manager,
        'dor_counselor':   counselor,
        'counseling_logs': counseling_logs,
        **defaults,
    })