from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class CaseStatusInfo(models.Model):
    case_status_code = models.CharField(max_length=10, primary_key=True)
    case_description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.case_description}"

class MonthlyClientListingLog(models.Model):
    participant_id = models.CharField(max_length=20)
    case_status_code = models.ForeignKey(CaseStatusInfo, on_delete=models.SET_NULL, null=True)
    dor_counselor = models.CharField(max_length=100)
    fund_begin_date = models.DateField(null=True, blank=True)
    fund_end_date = models.DateField(null=True, blank=True)
    closure_date = models.DateField(null=True, blank=True)
    district = models.CharField(max_length=100)
    updated_date = models.DateField(auto_now_add=True)
    period = models.CharField(
        max_length=7,
        blank=False,
        help_text="e.g. 03-2025"
    )
    class Meta:
        # unique_together = (('participant_id', 'period'),)
        pass

    def __str__(self):
        return f"{self.participant_id} – {self.period or '(no period)'}"

class WaivUser(AbstractUser):
    """Extends Django’s built-in User: handles login, is_active, permissions, etc."""
    POSITION_CHOICES = (
        ("counselor",    "Counselor"),
        ("case_manager", "Case Manager"),
        # ("admin",        "Administrator"),
    )
    position = models.CharField(max_length=30, choices=POSITION_CHOICES, default="counselor")

class StudentPersonalInfo(models.Model):
    csulb_id = models.CharField(primary_key=True, max_length=15, db_column="csulb_id")
    participant_id = models.CharField(max_length=15, unique=True, db_column="participant_id")
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
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
    job_placement = models.TextField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    csulb_id = models.ForeignKey(StudentPersonalInfo, on_delete=models.CASCADE, null=False, blank=False, db_column="csulb_id")
    case_status_code = models.ForeignKey(CaseStatusInfo, on_delete=models.SET_NULL, null=True)
    updated_date = models.DateTimeField(auto_now_add=True)

class CheckinSimplicity(models.Model):
    # Change this from a ForeignKey to a simple CharField:
    csulb_id      = models.CharField(
        max_length=20,
        help_text="Raw Participant_ID from Simplicity (no FK lookup).",
    )
    date_checkin  = models.DateField(null=True, blank=True)
    event_type    = models.CharField(max_length=255)
    staff         = models.ForeignKey(
        WaivUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="checkin_counselor"
    )
    name          = models.CharField(max_length=255)
    location      = models.CharField(max_length=255)
    imported_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.csulb_id} @ {self.date_checkin} ({self.event_type})"

class WaivServiceInfo(models.Model):
    service_type = models.IntegerField(primary_key=True)
    service_description = models.CharField(max_length=255)

    def __str__(self):
        return self.service_description

class CounselingLog(models.Model):
    counsel_log_id = models.AutoField(primary_key=True)
    csulb_id = models.ForeignKey(StudentPersonalInfo, on_delete=models.CASCADE, null=True, blank=True, db_column="csulb_id")
    service_type = models.ForeignKey(WaivServiceInfo, on_delete=models.SET_NULL, null=True)
    staff        = models.ForeignKey(WaivUser,  on_delete=models.SET_NULL, null=True, related_name="sessions")
    date_checkin = models.DateField()
    case_note = models.TextField()
    updated_date = models.DateTimeField(auto_now_add=True)

class StudentDoc(models.Model):
    DOC_TYPE_CHOICES = [
        ('waivreferral', 'WAIV Referral Form'),
        ('dr260',         'DR 260 – Consent To Release'),
        ('dr215',         'DR 215 – Individualized Plan Employment (IPE)'),
        ('dr222',         'DR 222 – VR Services Application'),
        ('casenote',      'Case Note Authorization'),
    ]
    csulb_id       = models.ForeignKey(
                        StudentPersonalInfo,
                        on_delete=models.CASCADE,
                        null=False,
                        blank=False,
                        db_column="csulb_id"
                    )
    doc_name      = models.CharField(
                        max_length=20,
                        choices=DOC_TYPE_CHOICES
                    )
    received_date = models.DateField(null=True, blank=True)
    expiry_date   = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('csulb_id', 'doc_name')
        ordering = ['csulb_id', 'doc_name']

    def __str__(self):
        return f"{self.csulb_id}"

class StudentAcademicLog(models.Model):
    academic_log_id = models.AutoField(primary_key=True)
    csulb_id = models.OneToOneField(
        StudentPersonalInfo,
        on_delete=models.CASCADE,
        db_column="csulb_id",
        related_name="academic_log"
    )
    academic_plan   = models.CharField(max_length=100, null=True, blank=True)
    academic_level  = models.CharField(max_length=50,  null=True, blank=True)
    gpa             = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    academic_updated= models.DateTimeField(auto_now_add=True)
