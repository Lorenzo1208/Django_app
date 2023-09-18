from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('DOCTOR', 'Médecin'),
        ('PATIENT', 'Patient'),
    )

    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES, default='PATIENT') # Augmenté à 7
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    groups = models.ManyToManyField(
        'auth.Group', 
        blank=True, 
        related_name="custom_user_groups", 
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name="custom_user_permissions",
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    # autres champs spécifiques au profil du patient

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    medical_license_number = models.CharField(max_length=100, null=True, blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    # autres champs spécifiques au profil du médecin

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    # autres champs spécifiques au profil de l'administrateur

class GeneralHealthForm(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='general_health_forms')
    submission_date = models.DateTimeField(auto_now_add=True)
    # Ajoutez ici les champs spécifiques au formulaire de santé générale

class StressLevelForm(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='stress_level_forms')
    submission_date = models.DateTimeField(auto_now_add=True)
    # Ajoutez ici les champs spécifiques au formulaire de niveau de stress

class DataAnalysis(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='data_analyses')
    analysis_type = models.CharField(max_length=100)
    date_conducted = models.DateTimeField(auto_now_add=True)
    results = models.TextField()
    # autres champs pour stocker les résultats des analyses de données

