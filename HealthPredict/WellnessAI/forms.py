from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Doctor

from .models import Appointment

# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['doctor', 'name', 'email', 'date', 'time', 'phone']
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),
#             'time': forms.TimeInput(attrs={'type': 'time'}),
#         }

from django import forms
# from .models import BasicDetails, Symptom

# class BasicDetailsForm(forms.ModelForm):
#     class Meta:
#         model = BasicDetails
#         fields = ['name', 'age', 'gender']  # Include any other fields

# class SymptomForm(forms.ModelForm):
#     class Meta:
#         model = Symptom
#         fields = ['symptoms']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'experience', 'contact', 'email', 'clinic_address']

