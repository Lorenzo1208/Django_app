from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime, timedelta
from django.conf import settings

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

class DataAnalysis(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='data_analyses')
    analysis_type = models.CharField(max_length=100)
    date_conducted = models.DateTimeField(auto_now_add=True)
    results = models.TextField()
    # autres champs pour stocker les résultats des analyses de données

class PatientDailyForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    # Informations générales
    poids = models.FloatField(validators=[MinValueValidator(30.0), MaxValueValidator(300.0)])
    tour_de_taille = models.IntegerField(validators=[MinValueValidator(40), MaxValueValidator(200)])

    # Informations cardiaques et tension artérielle
    frequence_cardiaque = models.IntegerField(validators=[MinValueValidator(40), MaxValueValidator(200)])
    tension_arterielle_matin_systolique = models.IntegerField(validators=[MinValueValidator(80), MaxValueValidator(200)])
    tension_arterielle_soir_systolique = models.IntegerField(validators=[MinValueValidator(80), MaxValueValidator(200)])
    tension_arterielle_matin_diastolique = models.IntegerField(validators=[MinValueValidator(50), MaxValueValidator(150)])
    tension_arterielle_soir_diastolique = models.IntegerField(validators=[MinValueValidator(50), MaxValueValidator(150)])
    symptomes_cardiovasculaires = models.TextField()

    # Prise de médicaments
    nombre_medicaments_jour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    oublie_medicament_matin = models.BooleanField(null=True)
    oublie_medicament_soir = models.BooleanField(null=True)
    effets_secondaires = models.BooleanField(null=True)
    symptomes_particuliers = models.BooleanField(null=True)
    description_effets_symptomes = models.TextField()

    # Alimentation et activité physique
    consommation_alcool = models.BooleanField(null=True)
    grignotage_sucre = models.BooleanField(null=True)
    grignotage_sale = models.BooleanField(null=True)
    nombre_repas_jour = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    quantite_eau = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    quantite_alcool = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    activite_physique = models.BooleanField(null=True)
    nature_activite_physique = models.CharField(max_length=100, null=True)
    duree_activite_physique = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)], null=True)

    # Symptômes supplémentaires
    presence_dyspnee = models.BooleanField(null=True)
    presence_oedeme = models.BooleanField(null=True)
    presence_episode_infectieux = models.BooleanField(null=True)
    presence_fievre = models.BooleanField(null=True)
    presence_palpitation = models.BooleanField(null=True)
    presence_douleur_thoracique = models.BooleanField(null=True)
    presence_malaise = models.BooleanField(null=True)
    
    # Informations sur les épisodes spécifiques
    heure_debut_palpitations = models.TimeField(null=True)
    duree_palpitations = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)], null=True)
    heure_debut_douleurs_thoraciques = models.TimeField(null=True)
    duree_douleurs_thoraciques = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)], null=True)
    heure_debut_malaises = models.TimeField(null=True)
    duree_malaises = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)], null=True)

    def save(self, *args, **kwargs):
        if not PatientDailyForm.objects.filter(user=self.user, date=datetime.now().date()).exists():
            if self.user.user_type == 'PATIENT':
                super().save(*args, **kwargs)
            else:
                raise ValueError("Seuls les patients peuvent soumettre ce formulaire")
        else:
            raise ValueError("Vous ne pouvez soumettre ce formulaire qu'une fois par jour")

class StressEvaluationForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    CHOICES = [
        (0, "0"),
        (1, "1"),
        (5, "5"),
        (10, "10"),
    ]
    
    SYMPTOMS = [
    'irritabilite', 
    'sentiments_depressifs', 
    'bouche_seche_ou_gorge_seche', 
    'actions_ou_gestes_impulsifs', 
    'grincement_des_dents', 
    'difficulte_a_rester_assis', 
    'cauchemars', 
    'diarrhee', 
    'attaques_verbales_envers_quelquun', 
    'hauts_et_bas_emotifs', 
    'grande_envie_de_pleurer', 
    'grande_envie_de_fuir', 
    'grande_envie_de_faire_mal', 
    'pensees_embrouillees', 
    'debit_plus_rapide', 
    'fatigue_ou_lourdeur_generalisees', 
    'sentiment_detre_surchargé', 
    'sentiment_detre_emotivement_fragile', 
    'sentiment_de_tristesse', 
    'sentiment_danxiete', 
    'tension_emotionnelle', 
    'hostilite_envers_les_autres', 
    'tremblements_ou_gestes_nerveux', 
    'begaiements_ou_hesitations_verbales', 
    'incapacite_ou_difficulte_a_se_concentrer', 
    'difficulte_a_organiser_ses_pensees', 
    'difficulte_a_dormir_toute_la_nuit_sans_se_reveiller', 
    'besoin_frequent_duriner', 
    'maux_destomac_ou_difficultes_a_digerer', 
    'geste_ou_sentiment_dimpatience', 
    'maux_de_tete', 
    'douleurs_au_dos_ou_a_la_nuque', 
    'perte_ou_gain_dappetit', 
    'perte_dinteret_pour_le_sexe', 
    'oublis_frequents', 
    'douleurs_ou_serrements_a_la_poitrine', 
    'conflits_significatifs_avec_les_autres', 
    'difficulte_a_se_lever_apres_le_sommeil', 
    'sentiment_que_les_choses_sont_hors_de_controle', 
    'mouvements_de_retrait_disolement', 
    'difficulte_a_sendormir', 
    'difficulte_a_se_remettre_dun_evenement_contrariant', 
    'mains_moites'
]

    total_impact_du_stress_dans_votre_vie_actuelle = models.IntegerField(default=0, blank=True)

    def save(self, *args, **kwargs):
        if not StressEvaluationForm.objects.filter(user=self.user, date__gte=datetime.now().date() - timedelta(days=14)).exists():
            super().save(*args, **kwargs)
        else:
            raise ValueError("Vous ne pouvez soumettre ce formulaire qu'une fois toutes les deux semaines")

for symptom in StressEvaluationForm.SYMPTOMS:
    field = models.IntegerField(choices=StressEvaluationForm.CHOICES, verbose_name=symptom)
    setattr(StressEvaluationForm, symptom, field)

class TestModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # Permettre la valeur nulle (null)
)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

