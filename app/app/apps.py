from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'app'  # Assurez-vous que cela correspond au nom de votre dossier d'application

    def ready(self):
        import app.signals  # Importez vos signaux ici
