from django.db import models

class DorCounselor(models.Model):
    dor_counselor_id = models.AutoField(primary_key=True)
    dor_counselor_name = models.CharField(max_length=100)
    dor_counselor_email = models.EmailField()

    def __str__(self):
        return f"{self.dor_counselor_name}"


class CaseStatusInfo(models.Model):
    case_status_code = models.CharField(max_length=10, primary_key=True)
    case_description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.case_description}"


class MonthlyClientListingLog(models.Model):
    id = models.AutoField(primary_key=True)
    participant_id = models.CharField(max_length=20, unique=True)
    case_status_code = models.ForeignKey(CaseStatusInfo, on_delete=models.SET_NULL, null=True)
    dor_counselor = models.ForeignKey(DorCounselor, on_delete=models.SET_NULL, null=True)
    fund_begin_date = models.DateField()
    fund_end_date = models.DateField()
    district = models.CharField(max_length=100)
    updated_date = models.DateField()


class StudentPersonalInfo(models.Model):
    csulb_id = models.CharField(primary_key=True, max_length=15)
    participant_id = models.OneToOneField(
        MonthlyClientListingLog, on_delete=models.SET_NULL, null=True, blank=True
    )
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    birthdate = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    employ_goal = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    enrollment_date = models.DateField()
    updated_date = models.DateTimeField(auto_now_add=True)
    case_manager = models.CharField(max_length=100)
    intake_status = models.BooleanField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    csulb_id = models.ForeignKey(StudentPersonalInfo, on_delete=models.CASCADE, null=True, blank=True)
    case_status_code = models.ForeignKey(CaseStatusInfo, on_delete=models.SET_NULL, null=True)
    last_updated = models.DateField()


class WaivStaffInfo(models.Model):
    waiv_staff_id = models.AutoField(primary_key=True)
    waiv_staff_name = models.CharField(max_length=100)
    waiv_staff_email = models.EmailField()

    def __str__(self):
        return f"{self.waiv_staff_name}"


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
    date_checkin = models.DateField()
    case_note = models.TextField()


class StudentDoc(models.Model):
    csulb_id = models.OneToOneField(StudentPersonalInfo, on_delete=models.CASCADE, primary_key=True, null=True, blank=True)
    doc_name = models.CharField(max_length=255)
    received_date = models.DateField()


class DisabilityInfo(models.Model):
    csulb_id = models.OneToOneField(StudentPersonalInfo, on_delete=models.CASCADE, primary_key=True, null=True, blank=True)
    disabilityType = models.CharField(max_length=100)
    disabilityDetail = models.TextField()


class StudentAcademicLog(models.Model):
    academic_log_id = models.AutoField(primary_key=True)
    csulb_id = models.ForeignKey(StudentPersonalInfo, on_delete=models.CASCADE, null=True, blank=True)
    academic_plan = models.CharField(max_length=100)
    academic_level = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    updated_date = models.DateField()
