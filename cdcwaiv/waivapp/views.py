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


class StudentPersonalInfoView(generics.ListCreateAPIView):
    queryset = StudentPersonalInfo.objects.all()
    serializer_class = StudentPersonalInfoSerializer


class CaseStatusInfoView(generics.ListCreateAPIView):
    queryset = CaseStatusInfo.objects.all()
    serializer_class = CaseStatusInfoSerializer


class DorCounselorView(generics.ListCreateAPIView):
    queryset = DorCounselor.objects.all()
    serializer_class = DorCounselorSerializer


class WaivServiceInfoView(generics.ListCreateAPIView):
    queryset = WaivServiceInfo.objects.all()
    serializer_class = WaivServiceInfoSerializer


class WaivStaffInfoView(generics.ListCreateAPIView):
    queryset = WaivStaffInfo.objects.all()
    serializer_class = WaivStaffInfoSerializer


class StudentDocView(generics.ListCreateAPIView):
    queryset = StudentDoc.objects.all()
    serializer_class = StudentDocSerializer


class DisabilityInfoView(generics.ListCreateAPIView):
    queryset = DisabilityInfo.objects.all()
    serializer_class = DisabilityInfoSerializer


class MonthlyClientListingLogView(generics.ListCreateAPIView):
    queryset = MonthlyClientListingLog.objects.all()
    serializer_class = MonthlyClientListingLogSerializer


class StudentAcademicLogView(generics.ListCreateAPIView):
    queryset = StudentAcademicLog.objects.all()
    serializer_class = StudentAcademicLogSerializer


class StudentLogView(generics.ListCreateAPIView):
    queryset = StudentLog.objects.all()
    serializer_class = StudentLogSerializer


class CounselingLogView(generics.ListCreateAPIView):
    queryset = CounselingLog.objects.all()
    serializer_class = CounselingLogSerializer