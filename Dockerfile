FROM python:3.13-slim

# Définir le dossier de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    nodejs \
    npm \
    && apt-get clean

# Copier les fichiers de build Tailwind en premier
COPY theme/static_src/package.json theme/static_src/package-lock.json* /app/theme/static_src/

# Installer Tailwind + autres modules front
WORKDIR /app/theme/static_src
RUN npm install

# Revenir au dossier principal
WORKDIR /app

# Copier requirements.txt et installer les dépendances Python
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le reste du projet
COPY . .

# Collect static et compiler Tailwind
RUN python manage.py tailwind build && python manage.py collectstatic --noinput

# Commande de démarrage
CMD ["gunicorn", "projetDjango.wsgi:application", "--bind", "0.0.0.0:8000"]
