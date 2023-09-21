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
    doctor_profile = DoctorProfile.objects.get(user=request.user)
    patients = doctor_profile.patients.all()
    context = {'patients': patients}
    return render(request, 'doctor_dashboard.html', context)

@login_required
def patient_dashboard(request):
    patient_profile = PatientProfile.objects.get(user=request.user)
    doctors = patient_profile.doctors.all()
    context = {'doctors': doctors}
    return render(request, 'patient_dashboard.html', context)