from .models import *
from django import forms
class DegreeForm(forms.ModelForm):
    class Meta:
        model = Degree
        fields = ['course','deg']
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['course','deg','dept']
class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['course','deg','dept','sname','gender','fname','dob','addr','email','cno','pgroup','caste','rel','img','bat']
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = "__all__"



        

