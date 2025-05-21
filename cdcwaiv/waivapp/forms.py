from django import forms
from .models import StudentDoc, StudentPersonalInfo, WaivUser, CaseStatusInfo

class StaffChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.id} – {obj.first_name} {obj.last_name}"

DOC_TYPE_CHOICES = [
    ("waivreferral", "WAIV Referral Form"),
    ("dr260",        "DR 260 – Consent To Release"),
    ("dr215",        "DR 215 – Individualized Plan Employment (IPE)"),
    ("dr222",        "DR 222 – VR Services Application"),
    ("casenote",     "Case Note Authorization"),
]

class AddStudentForm(forms.ModelForm):
    # Choice fields with form-control
    ACADEMIC_LEVEL_CHOICES = [
        ("Freshman",  "Freshman"),
        ("Sophomore","Sophomore"),
        ("Junior",   "Junior"),
        ("Senior",   "Senior"),
        ("Master",   "Graduate Student"),
        ("Graduated","Graduated"),
    ]
    academic_level = forms.ChoiceField(
        label="Academic Level",
        choices=ACADEMIC_LEVEL_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    INTAKE_CHOICES = [
        (True, "Yes"),
        (False,"No"),
    ]
    intake_status = forms.TypedChoiceField(
        label="Intake Status",
        choices=INTAKE_CHOICES,
        coerce=lambda x: x == 'True',
        widget=forms.Select(attrs={"class": "form-control"})
    )

    DISABILITY_TYPE_CHOICES = [
        ("mental",       "Mental"),
        ("physical",     "Physical"),
        ("neurological", "Neurological"),
        ("combination",  "Combination"),
    ]
    disability_type = forms.ChoiceField(
        label="Disability Type",
        choices=DISABILITY_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Case dropdowns
    case_manager = StaffChoiceField(
        label="Case Manager",
        queryset=WaivUser.objects.filter(position="case_manager"),
        empty_label="— Select Case Manager —",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    dedicated_counselor = StaffChoiceField(
        label="Dedicated Counselor",
        queryset=WaivUser.objects.filter(position="counselor"),
        empty_label="— Select Counselor —",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Initial case status log
    case_status = forms.ModelChoiceField(
        label="Initial Case Status",
        queryset=CaseStatusInfo.objects.all(),
        required=False,
        empty_label="— Select Case Status —",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Date fields
    birthdate = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    enrollment_date = forms.DateField(
        label="Enrollment Date",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    # Simple CharFields
    csulb_id = forms.CharField(
        label="CSULB ID",
        max_length=15,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    participant_id = forms.CharField(
        label="Participant ID",
        max_length=15,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    employ_goal = forms.CharField(
        label="Employment Goal",
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    academic_plan = forms.CharField(
        label="Academic Plan",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    gpa = forms.DecimalField(
        label="GPA",
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0", "max": "4"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        label="Phone",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    city = forms.CharField(
        label="City",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    disability_detail = forms.CharField(
        label="Disability Detail",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    # Dynamically add document fields with proper widgets
    DOC_TYPE_CHOICES = DOC_TYPE_CHOICES
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for code, pretty in self.DOC_TYPE_CHOICES:
            self.fields[f"checkbox_{code}"] = forms.BooleanField(
                label=pretty,
                required=False,
                widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
            )
            self.fields[f"received_{code}"] = forms.DateField(
                label="Received Date",
                required=False,
                widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
            )
            self.fields[f"expiry_{code}"] = forms.DateField(
                label="Expiry Date",
                required=False,
                widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
            )

    class Meta:
        model = StudentPersonalInfo
        fields = [
            "csulb_id",
            "participant_id",
            "last_name",
            "first_name",
            "birthdate",
            "email",
            "phone",
            "city",
            "employ_goal",
            "enrollment_date",
            "intake_status",
            "disability_type",
            "disability_detail",
            "case_manager",
            "dedicated_counselor",
            # note: do NOT include `case_status` here
        ]
