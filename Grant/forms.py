from django import forms
from django.forms import ModelForm
from .models import Application

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ('projectTitle', 'projectDescription', 'additionalInformation', 'phoneNumber',)
        widgets = {
            'projectTitle': forms.TextInput(attrs={'class': 'form-control'}),
            'projectDescription': forms.TextInput(attrs={'class': 'form-control'}),
            'additionalInformation': forms.TextInput(attrs={'class': 'form-control'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
        }
