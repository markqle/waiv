from django.shortcuts import render
from rest_framework import generics
from .serializers import (
    CaseStatusInfoSerializer,
    DorCounselorSerializer,
    WaivServiceInfoSerializer,
    WaivStaffInfoSerializer,
    StudentPersonalInfoSerializer,
    StudentDocSerializer,
    DisabilityInfoSerializer,
    MonthlyClientListingLogSerializer,
    StudentAcademicLogSerializer,
    StudentLogSerializer,
    CounselingLogSerializer
)
from .models import (
    CaseStatusInfo,
    DorCounselor,
    WaivStaffInfo,
    WaivServiceInfo,
    StudentPersonalInfo,
    StudentDoc,
    DisabilityInfo,
    MonthlyClientListingLog,
    StudentAcademicLog,
    StudentLog,
    CounselingLog
)


class StudentPersonalInfoView(generics.CreateAPIView):
    queryset = StudentPersonalInfo.objects.all()
    serializer_class = StudentPersonalInfoSerializer


class CaseStatusInfoView(generics.CreateAPIView):
    queryset = CaseStatusInfo.objects.all()
    serializer_class = CaseStatusInfoSerializer


class DorCounselorView(generics.CreateAPIView):
    queryset = DorCounselor.objects.all()
    serializer_class = DorCounselorSerializer


class WaivServiceInfoView(generics.CreateAPIView):
    queryset = WaivServiceInfo.objects.all()
    serializer_class = WaivServiceInfoSerializer


class WaivStaffInfoView(generics.CreateAPIView):
    queryset = WaivStaffInfo.objects.all()
    serializer_class = WaivStaffInfoSerializer


class StudentDocView(generics.CreateAPIView):
    queryset = StudentDoc.objects.all()
    serializer_class = StudentDocSerializer


class DisabilityInfoView(generics.CreateAPIView):
    queryset = DisabilityInfo.objects.all()
    serializer_class = DisabilityInfoSerializer


class MonthlyClientListingLogView(generics.CreateAPIView):
    queryset = MonthlyClientListingLog.objects.all()
    serializer_class = MonthlyClientListingLogSerializer


class StudentAcademicLogView(generics.CreateAPIView):
    queryset = StudentAcademicLog.objects.all()
    serializer_class = StudentAcademicLogSerializer


class StudentLogView(generics.CreateAPIView):
    queryset = StudentLog.objects.all()
    serializer_class = StudentLogSerializer


class CounselingLogView(generics.CreateAPIView):
    queryset = CounselingLog.objects.all()
    serializer_class = CounselingLogSerializer