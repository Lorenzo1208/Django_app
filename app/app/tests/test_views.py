import random
from datetime import time, date
from django.test import TestCase
from django.urls import reverse
from app.models import User
from app.models import PatientDailyForm

# Vérifie que la vue d'accueil renvoie un statut HTTP 200 et utilise le bon template.
class HomeViewTest(TestCase):
    def test_home_view_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

# Simule une requête POST avec des données d'inscription valides.
# Vérifie que la réponse est une redirection (HTTP 302) et que l'utilisateur est créé.
class InscriptionViewTest(TestCase):
    def test_inscription_valid_post(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            # Incluez d'autres champs requis par votre InscriptionForm
        }
        response = self.client.post(reverse('inscription'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirection attendue
        self.assertTrue(User.objects.filter(username='testuser').exists())

# Prépare un utilisateur pour le test de connexion.
# Teste la connexion avec des identifiants valides et vérifie la redirection et la session utilisateur.
class ConnexionViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='testpassword')

    def test_connexion_valid_post(self):
        response = self.client.post(reverse('connexion'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Redirection attendue
        self.assertTrue('_auth_user_id' in self.client.session)

# Prépare un utilisateur et le connecte pour le test.
# generate_random_data crée des données de formulaire valides et aléatoires pour PatientDailyForm.
# test_patient_form_valid_post vérifie que la soumission du formulaire crée un nouvel enregistrement et redirige correctement.
# test_patient_form_cannot_be_submitted_twice vérifie qu'un formulaire ne peut pas être soumis deux fois avec les mêmes données pour le même utilisateur.
class PatientFormViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def generate_random_data(self):
        return {
            'poids': random.uniform(30.0, 300.0),
            'tour_de_taille': random.randint(40, 200),
            'frequence_cardiaque': random.randint(40, 200),
            'tension_arterielle_matin_systolique': random.randint(80, 200),
            'tension_arterielle_soir_systolique': random.randint(80, 200),
            'tension_arterielle_matin_diastolique': random.randint(50, 150),
            'tension_arterielle_soir_diastolique': random.randint(50, 150),
            'symptomes_cardiovasculaires': 'Test cardio',
            'nombre_medicaments_jour': random.randint(0, 50),
            'oublie_medicament_matin': random.choice([True, False]),
            'oublie_medicament_soir': random.choice([True, False]),
            'effets_secondaires': random.choice([True, False]),
            'symptomes_particuliers': random.choice([True, False]),
            'description_effets_symptomes': 'Description test',
            'consommation_alcool': random.choice([True, False]),
            'grignotage_sucre': random.choice([True, False]),
            'grignotage_sale': random.choice([True, False]),
            'nombre_repas_jour': random.randint(1, 10),
            'quantite_eau': random.uniform(0.0, 10.0),
            'quantite_alcool': random.uniform(0.0, 10.0),
            'activite_physique': random.choice([True, False]),
            'nature_activite_physique': 'Activité test',
            'duree_activite_physique': random.randint(0, 300),
            'presence_dyspnee': random.choice([True, False]),
            'presence_oedeme': random.choice([True, False]),
            'presence_episode_infectieux': random.choice([True, False]),
            'presence_fievre': random.choice([True, False]),
            'presence_palpitation': random.choice([True, False]),
            'presence_douleur_thoracique': random.choice([True, False]),
            'presence_malaise': random.choice([True, False]),
            'heure_debut_palpitations': time(random.randint(0, 23), random.randint(0, 59)),
            'duree_palpitations': random.randint(0, 300),
            'heure_debut_douleurs_thoraciques': time(random.randint(0, 23), random.randint(0, 59)),
            'duree_douleurs_thoraciques': random.randint(0, 300),
            'heure_debut_malaises': time(random.randint(0, 23), random.randint(0, 59)),
            'duree_malaises': random.randint(0, 300),
        }

    def test_patient_form_valid_post(self):
        form_data = self.generate_random_data()
        response = self.client.post(reverse('patient_form'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirection attendue
        self.assertTrue(PatientDailyForm.objects.filter(user=self.user).exists())

    def test_patient_form_cannot_be_submitted_twice(self):
        form_data = self.generate_random_data()
        response = self.client.post(reverse('patient_form'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirection attendue après la première soumission

        response = self.client.post(reverse('patient_form'), form_data)
        self.assertNotEqual(response.status_code, 302)  # La deuxième soumission ne devrait pas réussir

        # Vous pouvez également vérifier le nombre de PatientDailyForm créés pour cet utilisateur
        self.assertEqual(PatientDailyForm.objects.filter(user=self.user).count(), 1)