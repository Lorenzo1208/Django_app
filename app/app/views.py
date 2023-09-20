from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import InscriptionForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import StressEvaluationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import PatientForm  # Adjust the import path based on your project structure
from .models import PatientDailyForm  # Import your model here
from django.shortcuts import render, redirect
from .models import TestModel  # Importez le modèle TestModel
from django.shortcuts import render, redirect
from .forms import TestForm
from django.db import transaction
from django.contrib.auth.decorators import login_required 
from .models import StressEvaluationForm

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

from .forms import StressEvaluationForm as StressEvaluationFormForm
from .models import StressEvaluationForm as StressEvaluationFormModel

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


@login_required  
def test_form_view(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            with transaction.atomic():
                TestModel.objects.create(name=name, email=email, user=user)

            return redirect('success')
    else:
        form = TestForm()

    return render(request, 'test_form_template.html', {'form': form})

def success_view(request):
    return render(request, 'success_template.html') 