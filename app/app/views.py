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
from .forms import PatientForm  # Ajustez le chemin d'importation en fonction de la structure de votre projet

class PatientFormView(FormView):
    template_name = 'patient_form.html'  # Remplacez par le chemin de votre template
    form_class = PatientForm
    success_url = reverse_lazy('success')  # Remplacez par l'URL de votre choix

    def form_valid(self, form):
        # Ici, vous pouvez ajouter la logique pour gérer les données du formulaire validé, par exemple enregistrer les données dans la base de données
        return super().form_valid(form)

    def form_invalid(self, form):
        # Ici, vous pouvez ajouter une logique supplémentaire pour gérer les formulaires non valides si nécessaire
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
