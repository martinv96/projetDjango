# Image de base
FROM python:3.12-slim

# Définir le répertoire de travail dans le container
WORKDIR /app

# Copier les fichiers de ton projet dans le container
COPY . /app

# Installer les dépendances
RUN pip install -r requirements.txt

# Construire Tailwind et collecter les fichiers statiques
RUN python manage.py tailwind build && python manage.py collectstatic --noinput

# Commande pour lancer l'application
CMD ["gunicorn", "projetDjango.wsgi:application"]
