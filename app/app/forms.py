from django.contrib.auth.forms import UserCreationForm
from .models import User

class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type']
