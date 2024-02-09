#!/bin/sh
# Exécuter monitoring.py en arrière-plan
python monitoring.py &

# Lancer le serveur Django
exec python manage.py runserver 0.0.0.0:8000
