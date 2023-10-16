from app.models import DoctorProfile  # Assurez-vous que le chemin d'importation est correct

def user_role(request):
    if not request.user.is_authenticated:
        return {}

    try:
        doctor_profile = DoctorProfile.objects.get(user=request.user)
        return {'is_doctor': True}
    except DoctorProfile.DoesNotExist:
        return {'is_doctor': False}
