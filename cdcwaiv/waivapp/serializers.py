from rest_framework import serializers
from .models import (
    CaseStatusInfo,
    DorCounselor,
    MonthlyClientListingLog,
    WaivUser,
    WaivServiceInfo,
    StudentPersonalInfo,
    StudentDoc,
    StudentAcademicLog,
    StudentLog,
    CounselingLog
)


class CaseStatusInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStatusInfo
        fields = '__all__'


# class DorCounselorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DorCounselor
#         fields = '__all__'


class MonthlyClientListingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyClientListingLog
        fields = '__all__'


class WaivUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaivUser
        fields = '__all__'


class WaivServiceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaivServiceInfo
        fields = '__all__'


class StudentPersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPersonalInfo
        fields = '__all__'


class StudentDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDoc
        fields = '__all__'


class StudentAcademicLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAcademicLog
        fields = '__all__'


class StudentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLog
        fields = '__all__'


class CounselingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselingLog
        fields = '__all__'
