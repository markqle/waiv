from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# class DorCounselor(models.Model):
#     dor_counselor_id = models.AutoField(primary_key=True)
#     dor_counselor_name = models.CharField(max_length=100)
#     dor_counselor_email = models.EmailField()

#     def __str__(self):
#         return f"{self.dor_counselor_name}"
    
# class MonthlyClientListingLog(models.Model):
#     participant_id = models.CharField(max_length=20, unique=True, primary_key=True)
#     case_status_code = models.ForeignKey(CaseStatusInfo, on_delete=models.SET_NULL, null=True)
#     dor_counselor = models.ForeignKey(DorCounselor, on_delete=models.SET_NULL, null=True)
#     fund_begin_date = models.DateField()
#     fund_end_date = models.DateField(null=True, blank=True)
#     district = models.CharField(max_length=100)
#     last_updated = models.DateField()

class CaseStatusInfo(models.Model):
    case_status_code = models.CharField(max_length=10, primary_key=True)
    case_description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.case_description}"

class WaivStaffInfo(AbstractUser):
    POSITION_CHOICES = [
        ("counselor",    "Counselor"),
        ("case_manager", "Case Manager"),
        ("IT",          "IT"),
        ("admin",        "Administrator"),
    ]
    position        = models.CharField(max_length=30, choices=POSITION_CHOICES, default="counselor")
    is_case_manager = models.BooleanField(default=False)

class MonthlyClientListingLog(models.Model):
    participant_id = models.CharField(max_length=20, unique=True, primary_key=True)
    case_status_code = models.ForeignKey(CaseStatusInfo, on_delete=models.SET_NULL, null=True)
    dor_counselor = models.ForeignKey(DorCounselor, on_delete=models.SET_NULL, null=True)
    fund_begin_date = models.DateField()
    fund_end_date = models.DateField(null=True, blank=True)
    district = models.CharField(max_length=100)
    updated_date = models.DateField()

class WaivUser(AbstractUser):
    """Extends Django’s built-in User: handles login, is_active, permissions, etc."""
    POSITION_CHOICES = [
        ("counselor",    "Counselor"),
        ("case_manager", "Case Manager"),
        ("admin",        "Administrator"),
        # add more roles as needed
    ]
    position = models.CharField(max_length=30, choices=POSITION_CHOICES, default="counselor")


class StudentPersonalInfo(models.Model):
    csulb_id = models.CharField(primary_key=True, max_length=15)
    participant_id = models.CharField(max_length=15, unique=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    employ_goal = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    enrollment_date = models.DateField()
    intake_status = models.BooleanField()
    case_manager    = models.ForeignKey(
        WaivUser,
        limit_choices_to={"position": "case_manager"},
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="managed_students"
    )
    dedicated_staff = models.ForeignKey(
        WaivUser,
        limit_choices_to={"position": "counselor"},
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="dedicated_students"
    )
    DISABILITY_CHOICES = [
        ("mental",       "Mental"),
        ("physical",     "Physical"),
        ("neurological", "Neurological"),
        ("combination",  "Combination"),
    ]
    disability_type   = models.CharField(
        max_length=12,
        choices=DISABILITY_CHOICES,
        null=True, blank=True
    )
    disability_detail = models.TextField(null=True, blank=True)

    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    csulb_id = models.ForeignKey(StudentPersonalInfo, on_delete=models.CASCADE, null=False, blank=False)
    case_status_code = models.ForeignKey(CaseStatusInfo, on_delete=models.SET_NULL, null=True)
    last_updated = models.DateField()

class WaivServiceInfo(models.Model):
    service_type = models.IntegerField(primary_key=True)
    service_description = models.CharField(max_length=255)

    def __str__(self):
        return self.service_description

class CounselingLog(models.Model):
    counsel_log_id = models.AutoField(primary_key=True)
    csulb_id = models.ForeignKey(StudentPersonalInfo, on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.ForeignKey(WaivServiceInfo, on_delete=models.SET_NULL, null=True)
    staff        = models.ForeignKey(WaivUser,  on_delete=models.SET_NULL, null=True, related_name="sessions")
    date_checkin = models.DateField()
    case_note = models.TextField()
    updated_date = models.DateField()

class DocumentType(models.Model):
    code        = models.CharField(
        max_length=20,
        primary_key=True,
        choices=[
            ("IPE",                "IPE"),
            ("WAIV_REFERRAL_FORM", "WAIV Referral Form"),
            ("DR260",              "DR260"),
            ("DR222",              "DR222"),
            ("CASE_NOTE_AUTH",     "Case Note Authorization"),
        ]
    )
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.get_code_display()


class StudentDoc(models.Model):
    csulb_id = models.OneToOneField(StudentPersonalInfo, on_delete=models.CASCADE, primary_key=True, related_name='doc')
    received_date = models.DateField()
    file          = models.FileField(upload_to="student_docs/", null=True, blank=True)

    # New M2M field for the types
    doc_types     = models.ManyToManyField(
        DocumentType,
        blank=True,
        related_name="student_docs"
    )

    def __str__(self):
        return f"{self.student}: {', '.join(str(dt) for dt in self.doc_types.all())}"

class StudentAcademicLog(models.Model):
    academic_log_id = models.AutoField(primary_key=True)
    csulb_id = models.ForeignKey(StudentPersonalInfo, on_delete=models.CASCADE, null=False, blank=False)
    academic_plan   = models.CharField(max_length=100, null=True, blank=True)
    academic_level  = models.CharField(max_length=50,  null=True, blank=True)
    gpa             = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    academic_updated= models.DateField(null=True, blank=True)
