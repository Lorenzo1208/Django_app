from django.contrib import admin
from .models import User, PatientProfile, DoctorProfile, DataAnalysis, PatientDailyForm, StressEvaluationForm
from django.contrib.auth.admin import UserAdmin

# Configuration personnalisée pour DoctorProfile
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'medical_license_number', 'specialty')
    filter_horizontal = ('patients',)  # Facilite la gestion des relations ManyToMany

# Configuration personnalisée pour PatientProfile
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'address')

# Enregistrement des modèles avec leurs configurations personnalisées
# admin.site.register(User)
admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(DataAnalysis)
admin.site.register(PatientDailyForm)
admin.site.register(StressEvaluationForm)
admin.site.register(User, UserAdmin)