"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import home, m, inscription, connexion  # Importez la vue hello_world depuis l'application app
from .views import PatientFormView
from .views import StressEvaluationForm
from . import views
from django.contrib.auth import views as auth_views
from .views import division_par_zero


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Ajoutez ce chemin pour la vue hello_world
    path('m/', m, name='m'),
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('patient_form/', PatientFormView.as_view(), name='patient_form'),
    path('stress_from/', views.evaluate_stress, name='evaluate_stress'),
    path('success/', views.success_view, name='success'),  # Remplacez views.success_view par la vue que vous souhaitez afficher après la soumission du formulaire
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('monitoring/', views.monitoring, name='monitoring'),
    path('test_view/', views.test_view, name='test_view'),
    path('division_par_zero/', views.division_par_zero, name='division_par_zero'),
]