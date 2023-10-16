# dans le fichier create_fake_users.py sous l'app django correspondante
from django.core.management.base import BaseCommand
from app.forms import InscriptionForm
from django.contrib.auth import get_user_model
from app.models import StressEvaluationForm
from app.models import PatientDailyForm
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate fake user data and stress evaluation forms for testing'

    def handle(self, *args, **kwargs):
        fake = Faker(['fr_FR'])
        User = get_user_model()

        for _ in range(10):  # Ajustez la plage selon le nombre d'utilisateurs à générer
            username = fake.user_name()
            while User.objects.filter(username=username).exists():  # Vérifiez si le nom d'utilisateur existe déjà
                username = fake.user_name()  # Génère un nouveau nom d'utilisateur si nécessaire

            form_data = {
                'username': username,  # Utilisez le nom d'utilisateur unique généré
                'email': fake.email(),
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'password1': 'Tabouret12.',  # Mot de passe temporaire
                'password2': 'Tabouret12.',  # Mot de passe temporaire
            }

            user_form = InscriptionForm(form_data)
            if user_form.is_valid():
                user = user_form.save()
                
                # Remplissage du formulaire d'évaluation du stress
                stress_form = StressEvaluationForm(user=user)
                for symptom in StressEvaluationForm.SYMPTOMS:
                    setattr(stress_form, symptom, random.choice(StressEvaluationForm.CHOICES)[0])
                stress_form.total_impact_du_stress_dans_votre_vie_actuelle = random.randint(0, 100)
                stress_form.score = random.randint(0, 100)
                try:
                    stress_form.save()
                except ValueError as e:
                    print(f"Could not save StressEvaluationForm for user {user.username}: {e}")

            else:
                print(f'Failed to create user: {user_form.errors}')

        patients = User.objects.filter(user_type='PATIENT')  # Récupérer tous les utilisateurs de type 'PATIENT'

        for patient in patients:  # Itérer sur chaque patient
            if not PatientDailyForm.objects.filter(user=patient, date=datetime.now().date()).exists():
                daily_form = PatientDailyForm(
                    user=patient, 
                    poids=random.uniform(30.0, 300.0),
                    tour_de_taille=random.randint(40, 200),
                    frequence_cardiaque=random.randint(40, 200),
                    tension_arterielle_matin_systolique=random.randint(80, 200),
                    tension_arterielle_soir_systolique=random.randint(80, 200),
                    tension_arterielle_matin_diastolique=random.randint(50, 150),
                    tension_arterielle_soir_diastolique=random.randint(50, 150),
                    symptomes_cardiovasculaires=fake.sentence(),
                    nombre_medicaments_jour=random.randint(0, 50),
                    oublie_medicament_matin=random.choice([True, False]),
                    oublie_medicament_soir=random.choice([True, False]),
                    effets_secondaires=random.choice([True, False]),
                    symptomes_particuliers=random.choice([True, False]),
                    description_effets_symptomes=fake.text(),
                    consommation_alcool=random.choice([True, False]),
                    grignotage_sucre=random.choice([True, False]),
                    grignotage_sale=random.choice([True, False]),
                    nombre_repas_jour=random.randint(1, 10),
                    quantite_eau=random.uniform(0.0, 10.0),
                    quantite_alcool=random.uniform(0.0, 10.0),
                    activite_physique=random.choice([True, False]),
                    nature_activite_physique=fake.word(),
                    duree_activite_physique=random.randint(0, 300),
                    presence_dyspnee=random.choice([True, False]),
                    presence_oedeme=random.choice([True, False]),
                    presence_episode_infectieux=random.choice([True, False]),
                    presence_fievre=random.choice([True, False]),
                    presence_palpitation=random.choice([True, False]),
                    presence_douleur_thoracique=random.choice([True, False]),
                    presence_malaise=random.choice([True, False]),
                    heure_debut_palpitations=fake.time(),
                    duree_palpitations=random.randint(0, 300),
                    heure_debut_douleurs_thoraciques=fake.time(),
                    duree_douleurs_thoraciques=random.randint(0, 300),
                    heure_debut_malaises=fake.time(),
                    duree_malaises=random.randint(0, 300)
                )
                try:
                    daily_form.save()
                    self.stdout.write(self.style.SUCCESS(f'Formulaire quotidien soumis pour {patient.username}'))
                except ValueError as e:
                    self.stdout.write(self.style.ERROR(f'Erreur lors de la soumission du formulaire quotidien pour {patient.username}: {e}'))
                    