from django.urls import path
from .views import (
    StudentPersonalInfoView,
    CaseStatusInfoView,
    DorCounselorView,
    WaivServiceInfoView,
    WaivStaffInfoView,
    StudentDocView,
    DisabilityInfoView,
    MonthlyClientListingLogView,
    StudentAcademicLogView,
    StudentLogView,
    CounselingLogView
)

urlpatterns = [
    path('student_personal_info/', StudentPersonalInfoView.as_view()),
    path('case_status_info/', CaseStatusInfoView.as_view()),
    path('dor_counselor/', DorCounselorView.as_view()),
    path('waiv_service_info/', WaivServiceInfoView.as_view()),
    path('waiv_staff_info/', WaivStaffInfoView.as_view()),
    path('student_doc/', StudentDocView.as_view()),
    path('disability_info/', DisabilityInfoView.as_view()),
    path('monthly_client_listing_log/', MonthlyClientListingLogView.as_view()),
    path('student_academic_log/', StudentAcademicLogView.as_view()),
    path('student_log/', StudentLogView.as_view()),
    path('counseling_log/', CounselingLogView.as_view())
]