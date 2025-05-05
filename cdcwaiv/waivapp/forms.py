from django import forms
from .models import StudentDoc

class StudentDocForm(forms.ModelForm):
    class Meta:
        model = StudentDoc
        fields = ["csulb_id", "received_date", "file", "doc_types"]
        widgets = {
            "doc_types": forms.CheckboxSelectMultiple
        }
