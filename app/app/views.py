from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import InscriptionForm

from django.contrib.auth import login as auth_login
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def m(request):
    return render(request, 'm.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

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

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import PatientForm  # Adjust the import path based on your project structure
from .models import PatientDailyForm  # Import your model here

class PatientFormView(FormView):
    template_name = 'patient_form.html' 
    form_class = PatientForm
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        # Create a new instance of the model and populate it with form data
        patient_daily_form = form.save(commit=False)  # Don't save it to the database yet

        # You can set any additional fields on the model here if needed
        patient_daily_form.user = self.request.user  # Assuming you want to associate the form with the logged-in user

        # Now, save the model instance to the database
        patient_daily_form.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle invalid form submission here if needed
        return super().form_invalid(form)

from django.shortcuts import render, redirect
from .forms import StressEvaluationForm

def evaluate_stress(request):
    if request.method == 'POST':
        form = StressEvaluationForm(request.POST)
        if form.is_valid():
            total_score = sum(int(value) for value in form.cleaned_data.values() if value not in [None, ''])
            # Vous pouvez enregistrer total_score dans votre base de données ou le traiter comme vous le souhaitez
            return render(request, 'results_template.html', {'total_score': total_score})
    else:
        form = StressEvaluationForm()

    return render(request, 'form_template.html', {'form': form})

from django.shortcuts import render, redirect
from .models import TestModel  # Importez le modèle TestModel
from django.shortcuts import render, redirect
from .forms import TestForm
from django.contrib.auth.decorators import login_required  # Importez le décorateur login_required

@login_required  # Appliquez le décorateur login_required pour vérifier que l'utilisateur est connecté
def test_form_view(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            # Capturer l'utilisateur connecté
            user = request.user

            # Processus de sauvegarde du formulaire
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Créez et sauvegardez le modèle avec l'utilisateur connecté associé
            test_model = TestModel(name=name, email=email, user=user)
            test_model.save()

            # Redirigez vers la page de réussite
            return redirect('success')
    else:
        form = TestForm()

    return render(request, 'test_form_template.html', {'form': form})

def success_view(request):
    return render(request, 'success_template.html') 