from django.contrib import admin
from .models import User, PatientProfile, DoctorProfile, AdminProfile, DataAnalysis, PatientDailyForm, StressEvaluationForm, TestModel

admin.site.register(User)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(AdminProfile)
admin.site.register(DataAnalysis)
admin.site.register(PatientDailyForm)
admin.site.register(StressEvaluationForm)
admin.site.register(TestModel)

