from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import InscriptionForm, StressEvaluationForm, PatientForm, StressEvaluationForm as StressEvaluationFormForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import PatientDailyForm, StressEvaluationForm as StressEvaluationFormModel
from .models import DoctorProfile, PatientProfile
from django.db import transaction
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.db.models import Count, F
from django.utils import timezone
from datetime import timedelta
from app.models import DoctorProfile, PatientDailyForm, StressEvaluationForm
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'home.html')

def m(request):
    return render(request, 'm.html')

def deconnexion_view(request):
    # Déconnecte l'utilisateur
    logout(request)
    # Redirige vers la page d'accueil
    return redirect('home')

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie")
            return redirect('home')
        else:
            messages.error(request, "Erreur de connexion. Veuillez réessayer.")
            return redirect('connexion')
    else:
        return render(request, 'connexion.html')

class PatientFormView(FormView):
    template_name = 'patient_form.html' 
    form_class = PatientForm
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        try:
            patient_daily_form = form.save(commit=False)
            patient_daily_form.user = self.request.user
            patient_daily_form.save()
        except ValueError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

        return super().form_valid(form)
    
def evaluate_stress(request):
    if request.method == 'POST':
        form = StressEvaluationFormForm(request.POST)
        if form.is_valid():
            total_score = sum(int(value) for value in form.cleaned_data.values() if value not in [None, ''])
            
            # Enregistrez total_score dans la base de données
            if request.user.is_authenticated:
                StressEvaluationFormModel.objects.create(score=total_score, user=request.user)
            else:
                # Gérez le cas où l'utilisateur n'est pas connecté, si nécessaire
                StressEvaluationFormModel.objects.create(score=total_score)
            
            return render(request, 'results_template.html', {'total_score': total_score})
    else:
        form = StressEvaluationFormForm()

    return render(request, 'form_template.html', {'form': form})

def success_view(request):
    return render(request, 'success_template.html') 

@login_required
def doctor_dashboard(request):
    doctor_profile = get_object_or_404(DoctorProfile, user=request.user)
    patients = doctor_profile.patients.all()

    # Créer des tuples avec les données nécessaires pour chaque patient
    data_per_patient = [
        (
            patient.user,
            sum(StressEvaluationForm.objects.filter(user=patient.user).values_list('score', flat=True)),
            sum(PatientDailyForm.objects.filter(user=patient.user).values_list('frequence_cardiaque', flat=True))
        )
        for patient in patients
    ]

    # Trier les données en fonction du score de stress et de la fréquence cardiaque
    stress_sorted_data = sorted(data_per_patient, key=lambda x: x[1], reverse=True)
    heart_rate_sorted_data = sorted(data_per_patient, key=lambda x: x[2], reverse=True)

    # Extraire les labels et les données pour les graphiques
    stress_labels = [item[0].username for item in stress_sorted_data]
    stress_scores = [item[1] for item in stress_sorted_data]
    heart_rate_labels = [item[0].username for item in heart_rate_sorted_data]
    heart_rates = [item[2] for item in heart_rate_sorted_data]

    context = {
        'form_counts_per_patient': data_per_patient,  # Si vous en avez encore besoin pour d'autres parties de la vue
        'is_doctor': True,
        'stress_labels': stress_labels,
        'stress_scores': stress_scores,
        'heart_rate_labels': heart_rate_labels,
        'heart_rates': heart_rates,
    }

    return render(request, 'doctor_dashboard.html', context)


@login_required
def patient_dashboard(request):
    patient_profile = get_object_or_404(PatientProfile, user=request.user)
    doctors = patient_profile.doctors.all()
    context = {
        'doctors': doctors,
        'is_doctor': False,  # Ajouter cette ligne
    }
    return render(request, 'patient_dashboard.html', context)