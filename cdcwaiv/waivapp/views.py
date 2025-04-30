from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

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


class StudentPersonalInfoView(generics.ListAPIView):
    queryset = StudentPersonalInfo.objects.all()
    serializer_class = StudentPersonalInfoSerializer


class CaseStatusInfoView(generics.ListAPIView):
    queryset = CaseStatusInfo.objects.all()
    serializer_class = CaseStatusInfoSerializer


class DorCounselorView(generics.ListAPIView):
    queryset = DorCounselor.objects.all()
    serializer_class = DorCounselorSerializer


class WaivServiceInfoView(generics.ListAPIView):
    queryset = WaivServiceInfo.objects.all()
    serializer_class = WaivServiceInfoSerializer


class WaivStaffInfoView(generics.ListAPIView):
    queryset = WaivStaffInfo.objects.all()
    serializer_class = WaivStaffInfoSerializer


class StudentDocView(generics.ListAPIView):
    queryset = StudentDoc.objects.all()
    serializer_class = StudentDocSerializer


class DisabilityInfoView(generics.ListAPIView):
    queryset = DisabilityInfo.objects.all()
    serializer_class = DisabilityInfoSerializer


class MonthlyClientListingLogView(generics.ListAPIView):
    queryset = MonthlyClientListingLog.objects.all()
    serializer_class = MonthlyClientListingLogSerializer


class StudentAcademicLogView(generics.ListAPIView):
    queryset = StudentAcademicLog.objects.all()
    serializer_class = StudentAcademicLogSerializer


class StudentLogView(generics.ListAPIView):
    queryset = StudentLog.objects.all()
    serializer_class = StudentLogSerializer


class CounselingLogView(generics.ListAPIView):
    queryset = CounselingLog.objects.all()
    serializer_class = CounselingLogSerializer