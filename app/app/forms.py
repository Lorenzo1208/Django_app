from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type']

class PatientForm(forms.Form):
    # Informations générales
    poids = forms.FloatField(min_value=30.0, max_value=300.0, label='Poids (kg)')
    tour_de_taille = forms.IntegerField(min_value=40, max_value=200, label='Tour de taille (cm)')

    # Informations cardiaques et tension artérielle
    frequence_cardiaque = forms.IntegerField(min_value=40, max_value=200, label='Fréquence cardiaque (par minute)')
    tension_arterielle_matin_systolique = forms.IntegerField(min_value=80, max_value=200, label='Tension artérielle systolique (prise du matin)')
    tension_arterielle_soir_systolique = forms.IntegerField(min_value=80, max_value=200, label='Tension artérielle systolique (prise du soir)')
    tension_arterielle_matin_diastolique = forms.IntegerField(min_value=50, max_value=150, label='Tension artérielle diastolique (prise du matin)')
    tension_arterielle_soir_diastolique = forms.IntegerField(min_value=50, max_value=150, label='Tension artérielle diastolique (prise du soir)')
    symptomes_cardiovasculaires = forms.CharField(widget=forms.Textarea, label='Symptômes cardiovasculaires en quelques mots')

    # Prise de médicaments
    nombre_medicaments_jour = forms.IntegerField(min_value=0, max_value=50, label='Nombre de médicaments pris dans la journée')
    oublie_medicament_matin = forms.BooleanField(required=False, label='Oubli de prendre le(s) médicament(s) le matin')
    oublie_medicament_soir = forms.BooleanField(required=False, label='Oubli de prendre le(s) médicament(s) le soir')
    effets_secondaires = forms.BooleanField(required=False, label='Effets secondaires remarqués')
    symptomes_particuliers = forms.BooleanField(required=False, label='Symptômes particuliers remarqués')
    description_effets_symptomes = forms.CharField(widget=forms.Textarea, label='Effets secondaires et/ou symptômes particuliers en quelques mots')

    # Alimentation et activité physique
    consommation_alcool = forms.BooleanField(required=False, label='Consommation d\'alcool')
    grignotage_sucre = forms.BooleanField(required=False, label='Grignotage sucré')
    grignotage_sale = forms.BooleanField(required=False, label='Grignotage salé')
    nombre_repas_jour = forms.IntegerField(min_value=1, max_value=10, label='Nombre de repas pris durant la journée')
    quantite_eau = forms.FloatField(min_value=0.0, max_value=10.0, label='Quantité d\'eau bue en litre')
    quantite_alcool = forms.FloatField(min_value=0.0, max_value=10.0, label='Quantité d\'alcool consommé en litre')
    activite_physique = forms.BooleanField(required=False, label='Activité physique aujourd\'hui')
    nature_activite_physique = forms.CharField(max_length=100, label='Nature de votre activité physique')
    duree_activite_physique = forms.IntegerField(min_value=0, max_value=300, label='Durée de l\'activité physique en minutes')

    # Symptômes supplémentaires
    presence_dyspnee = forms.BooleanField(required=False, label='Présence de dyspnée')
    presence_oedeme = forms.BooleanField(required=False, label='Présence d\'oedème')
    presence_episode_infectieux = forms.BooleanField(required=False, label='Présence d\'épisode infectieux')
    presence_fievre = forms.BooleanField(required=False, label='Présence de fièvre')
    presence_palpitation = forms.BooleanField(required=False, label='Présence de palpitation')
    presence_douleur_thoracique = forms.BooleanField(required=False, label='Présence de douleur thoracique')
    presence_malaise = forms.BooleanField(required=False, label='Présence de malaise')
    
    # Informations sur les épisodes spécifiques
    heure_debut_palpitations = forms.TimeField(required=False, label='Indiquez l\'heure de début des palpitations')
    duree_palpitations = forms.IntegerField(min_value=0, max_value=300, required=False, label='Indiquez la durée totale des palpitations en minutes')
    heure_debut_douleurs_thoraciques = forms.TimeField(required=False, label='Indiquez l\'heure de début des douleurs thoraciques')
    duree_douleurs_thoraciques = forms.IntegerField(min_value=0, max_value=300, required=False, label='Indiquez la durée totale des douleurs thoraciques en minutes')
    heure_debut_malaises = forms.TimeField(required=False, label='Indiquez l\'heure de début des malaises')
    duree_malaises = forms.IntegerField(min_value=0, max_value=300, required=False, label='Indiquez la durée totale des malaises en minutes')

class StressEvaluationForm(forms.Form):
    CHOICES = [
        (0, "0"),
        (1, "1"),
        (5, "5"),
        (10, "10"),
    ]

    irritabilite = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    sentiments_depressifs = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    bouche_seche_ou_gorge_seche = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    actions_ou_gestes_impulsifs = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    grincement_des_dents = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    difficulte_a_rester_assis = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    cauchemars = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    diarrhee = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    attaques_verbales_envers_quelquun = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    hauts_et_bas_emotifs = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    grande_envie_de_pleurer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    grande_envie_de_fuir = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    grande_envie_de_faire_mal = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    pensees_embrouillees = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    debit_plus_rapide = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    fatigue_ou_lourdeur_generalisees = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    sentiment_detre_surchargé = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    sentiment_detre_emotivement_fragile = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    sentiment_de_tristesse = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    sentiment_danxiete = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    tension_emotionnelle = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    hostilite_envers_les_autres = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    tremblements_ou_gestes_nerveux = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    begaiements_ou_hesitations_verbales = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    incapacite_ou_difficulte_a_se_concentrer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    difficulte_a_organiser_ses_pensees = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    difficulte_a_dormir_toute_la_nuit_sans_se_reveiller = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    besoin_frequent_duriner = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    maux_destomac_ou_difficultes_a_digerer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    geste_ou_sentiment_dimpatience = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    maux_de_tete = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    douleurs_au_dos_ou_a_la_nuque = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    perte_ou_gain_dappetit = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    perte_dinteret_pour_le_sexe = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    oublis_frequents = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    douleurs_ou_serrements_a_la_poitrine = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    conflits_significatifs_avec_les_autres = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    difficulte_a_se_lever_apres_le_sommeil = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    sentiment_que_les_choses_sont_hors_de_controle = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    mouvements_de_retrait_disolement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    difficulte_a_sendormir = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    difficulte_a_se_remettre_dun_evenement_contrariant = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    mains_moites = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    total_impact_du_stress_dans_votre_vie_actuelle = forms.IntegerField(initial=0, required=False)
