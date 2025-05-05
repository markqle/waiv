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

    def __str__(self):
        return self.get_full_name() or self.username

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
    updated_date = models.DateTimeField(auto_now_add=True)
    intake_status = models.BooleanField()
    DISABILITY_TYPE_CHOICES = [
        ("mental",       "Mental"),
        ("physical",     "Physical"),
        ("neurological", "Neurological"),
        ("combination",  "Combination"),
    ]
    disability_type = models.CharField( max_length=12, choices=DISABILITY_TYPE_CHOICES, null=True, blank=True)
    disability_detail = models.TextField( null=True, blank=True, help_text="Provide any additional details about the student disability.")
    case_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'is_case_manager': True},
        related_name='managed_students'
    )
    assigned_counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='counseled_students'
    )

    class Meta:
        unique_together = ("csulb_id", "participant_id")
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    csulb_id = models.ForeignKey(StudentPersonalInfo, on_delete=models.CASCADE, null=False, blank=False)
    case_status_code = models.ForeignKey(CaseStatusInfo, on_delete=models.SET_NULL, null=True)
    updated_date = models.DateField()
    def __str__(self):
        return f"{self.csulb_id} – {self.case_status_code}"


class WaivServiceInfo(models.Model):
    service_type = models.IntegerField(primary_key=True)
    service_description = models.CharField(max_length=255)

    def __str__(self):
        return self.service_description


class CounselingLog(models.Model):
    counsel_log_id = models.AutoField(primary_key=True)
    csulb_id = models.ForeignKey(StudentPersonalInfo, on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.ForeignKey(WaivServiceInfo, on_delete=models.SET_NULL, null=True)
    waiv_staff = models.ForeignKey(WaivStaffInfo, on_delete=models.SET_NULL, null=True)
    case_note = models.TextField()
    updated_date = models.DateField()


class StudentDoc(models.Model):
    csulb_id = models.OneToOneField(StudentPersonalInfo, on_delete=models.CASCADE, primary_key=True)
    doc_name = models.CharField(max_length=255)
    updated_date = models.DateField()
    file  = models.FileField( upload_to="student_docs/", null=True, blank=True)


class StudentAcademicLog(models.Model):
    academic_log_id = models.AutoField(primary_key=True)
    csulb_id = models.ForeignKey(StudentPersonalInfo, on_delete=models.CASCADE, null=False, blank=False)
    academic_plan = models.CharField(max_length=100)
    academic_level = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    updated_date = models.DateField()
