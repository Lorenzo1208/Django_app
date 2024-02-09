# Utiliser une image Python officielle comme base
FROM python:3.10.0a6-alpine3.13

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances et les installer
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier le reste du code de l'application
COPY . /app

# Exposer le port sur lequel l'application s'exécute
EXPOSE 8000

# Commande pour lancer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Copier start.sh dans le conteneur
COPY start.sh /app

# Rendre start.sh exécutable
RUN chmod +x /app/start.sh

# Utiliser start.sh comme commande par défaut
CMD ["/app/start.sh"]
