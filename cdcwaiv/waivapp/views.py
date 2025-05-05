from django.shortcuts import render, redirect
from rest_framework import generics
from .forms import StudentDocForm
from .serializers import (
    CaseStatusInfoSerializer,
    DorCounselorSerializer,
    WaivServiceInfoSerializer,
    WaivUserSerializer,
    StudentPersonalInfoSerializer,
    StudentDocSerializer,
    MonthlyClientListingLogSerializer,
    StudentAcademicLogSerializer,
    StudentLogSerializer,
    CounselingLogSerializer
)
from .models import (
    CaseStatusInfo,
    DorCounselor,
    WaivUser,
    WaivServiceInfo,
    StudentPersonalInfo,
    StudentDoc,
    MonthlyClientListingLog,
    StudentAcademicLog,
    StudentLog,
    CounselingLog
)

def showDemoPage(request):
    return render(request, "demo.html")

def upload_doc(request):
    if request.method == "POST":
        form = StudentDocForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success_url")
    else:
        form = StudentDocForm()
    return render(request, "upload_doc.html", {"form": form})


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


class WaivUserView(generics.ListAPIView):
    queryset = WaivUser.objects.all()
    serializer_class = WaivUserSerializer


class StudentDocView(generics.ListAPIView):
    queryset = StudentDoc.objects.all()
    serializer_class = StudentDocSerializer


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
