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

    # Récupérer les types de formulaires et le nombre de soumissions pour chaque patient
    form_counts_per_patient = []
    for patient in patients:
        user = patient.user
        # Compter les formulaires de StressEvaluationForm
        stress_form_count = StressEvaluationForm.objects.filter(user=user).count()
        # Compter les formulaires de PatientDailyForm
        daily_form_count = PatientDailyForm.objects.filter(user=user).count()

        form_counts_per_patient.append((user, {
            'stress_form_count': stress_form_count,
            'daily_form_count': daily_form_count,
        }))

    context = {
        'form_counts_per_patient': form_counts_per_patient,
        'is_doctor': True,  # Ajouter cette ligne
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