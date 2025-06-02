FROM python:3.13-slim

# Définir le dossier de travail
WORKDIR /app

# Installer les dépendances système nécessaires (et Node.js via NodeSource)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    gnupg \
    libpq-dev \
    python3-dev \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Copier les fichiers de build Tailwind en premier (meilleure gestion du cache Docker)
COPY theme/static_src/package.json theme/static_src/package-lock.json* /app/theme/static_src/

# Installer les dépendances npm
WORKDIR /app/theme/static_src
RUN npm install

# Revenir au dossier principal
WORKDIR /app

# Copier requirements.txt et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le reste du projet (code source Django)
COPY . .

# Compiler Tailwind et collecter les fichiers statiques
RUN python manage.py tailwind install \
    && python manage.py tailwind build \
    && python manage.py collectstatic --noinput

# Commande de démarrage
CMD ["gunicorn", "projetDjango.wsgi:application", "--bind", "0.0.0.0:8000"]
