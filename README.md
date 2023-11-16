
# DoctoLib - Application Web pour Médecins

DoctoLib est une application Web Django développée pour permettre aux professionnels de santé de mener des enquêtes de santé publique et de gérer leurs patients. L'application offre des fonctionnalités pour les administrateurs, médecins et patients, avec une emphase sur la sécurité et la confidentialité des données.

## Prérequis

- Python 3.8 ou supérieur
- pip
- virtualenv (optionnel, mais recommandé)

## Installation

1. **Clonez le dépôt :**
   ```bash
   git clone [URL_DU_DÉPÔT]
   cd doctolib
   ```

2. **Configurez un environnement virtuel :**
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows, utilisez `env\Scripts\activate`
   ```

3. **Installez les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialisez la base de données :**
   ```bash
   python manage.py migrate
   ```

5. **Créez un superutilisateur :**
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancez le serveur :**
   ```bash
   python manage.py runserver
   ```

   Accédez à http://localhost:8000 pour utiliser l'application.

## Réutilisation du Dump de la Base de Données

Pour initialiser votre base de données avec les données préexistantes fournies dans le fichier db.json, suivez ces étapes :

1. **Placez le fichier db.json dans le répertoire principal du projet :**
   Assurez-vous que le fichier db.json est accessible depuis le répertoire racine de votre projet Django.

2. **Initialisez votre base de données (si ce n'est pas déjà fait) :**
   ```bash
   python manage.py migrate
   ```

3. **Chargez les données depuis le fichier db.json :**
   ```bash
   python manage.py loaddata db.json
   ```

   Cette commande peuplera votre base de données avec les données contenues dans db.json.

4. **Vérifiez les données :**
   Après avoir chargé les données, il est conseillé de vérifier si elles ont été importées correctement. Vous pouvez le faire en utilisant l'interface d'administration Django ou en exécutant des requêtes de test via le shell Django.

5. **Lancez le serveur :**
   ```bash
   python manage.py runserver
   ```

   Accédez à http://localhost:8000 dans votre navigateur pour interagir avec l'application.

## Fonctionnalités

- **Administration :** Gestion des comptes médecins et patients, attribution des patients, et visualisation des historiques.
- **Médecins :** Gestion des comptes patients, et analyse des données de santé.
- **Patients :** Soumission des informations via des formulaires de santé.

## Sécurité des Données

- Aucune information personnelle n'est stockée directement. Un système d'ID unique est utilisé pour chaque utilisateur.
- Les utilisateurs doivent modifier leur mot de passe à la première connexion.
- Recommandations de mot de passe sécurisé intégrées.

## Tests

- Tests unitaires avec un coverage de 70% minimum.
- Pour exécuter les tests : `python manage.py test`
