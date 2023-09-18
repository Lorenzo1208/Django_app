from django.contrib import admin
from .models import User, PatientProfile, DoctorProfile, AdminProfile, GeneralHealthForm, StressLevelForm, DataAnalysis

admin.site.register(User)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(AdminProfile)
admin.site.register(GeneralHealthForm)
admin.site.register(StressLevelForm)
admin.site.register(DataAnalysis)
