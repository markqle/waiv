# waivapp/StaffViews.py

from django.shortcuts      import render, redirect, get_object_or_404
from django.contrib        import messages
from django.urls           import reverse
from waivapp.models        import (
    StudentPersonalInfo,
    WaivServiceInfo,
    WaivUser,
    CounselingLog,
    StudentDoc,
    StudentLog,
    StudentAcademicLog,
    CaseStatusInfo
)
from django.db.models import Q
from waivapp import manager
from datetime import timedelta
from django.utils import timezone
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from waivapp.forms         import AddStudentForm
from django.db import transaction
from django.db.models import Q, Count
from django.db import transaction
import json
# ——————————————————————————————————————————————————————————————
# HOME
# ——————————————————————————————————————————————————————————————

def staff_home(request):
    # define the 1-month lookback
    today = timezone.now().date()
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

    return render(request, "staff_template/staff_home_template.html", {
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


# ——————————————————————————————————————————————————————————————
# COUNSELING
# ——————————————————————————————————————————————————————————————

def add_counseling(request):
    students = StudentPersonalInfo.objects.all()
    counselors = WaivUser.objects.filter(position__in=['counselor', 'case_manager'])
    service_types = WaivServiceInfo.objects.all()
    return render(request,"staff_template/add_counseling_template.html",{
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
            messages.success(request, "Successfully added counseling session.")
            return redirect('staff_add_counseling')
        except Exception as e:
            messages.error(request, f"Failed to Add new counseling note: {e}")
            return redirect('staff_add_counseling')

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
    return render(request, "staff_template/view_counseling_template.html", {
        'students':    students_qs,
        'search':      search,
        'student':     student,
        'logs':        logs,
        'start_date':  start_date,
        'end_date':    end_date,
    })

# ——————————————————————————————————————————————————————————————
# STUDENTS
# ——————————————————————————————————————————————————————————————

def manage_student(request):
    qs = StudentPersonalInfo.objects.select_related(
        'case_manager','dedicated_staff'
    ).all()
    return render(request, "staff_template/manage_student_template.html", {
        "students": qs,
    })

def view_student(request, csulb_id):
    student      = get_object_or_404(StudentPersonalInfo, csulb_id=csulb_id)
    academic_log = getattr(student, 'academic_log', None)
    return render(request, "staff_template/view_student_template.html", {
        "student":      student,
        "academic_log": academic_log,
    })


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
    return render(request, "staff_template/edit_student_template.html", {
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
    return redirect('staff_edit_student', csulb_id=csulb_id)
