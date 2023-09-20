from django.contrib.auth.forms import UserCreationForm
from .models import User, PatientDailyForm, StressEvaluationForm as StressEvaluationModel
from django import forms
from datetime import datetime, timedelta

class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientDailyForm
        fields = '__all__'
        exclude = ['user', 'date']  # Nous excluons user et date car ils seront gérés séparément

class StressEvaluationForm(forms.Form):
    CHOICES = [
        (0, "0"),
        (1, "1"),
        (5, "5"),
        (10, "10"),
    ]

    for symptom in StressEvaluationModel.SYMPTOMS:
        locals()[symptom] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label=symptom.replace('_', ' '))


class TestForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100)
    email = forms.EmailField(label="Email")