FROM python:3.13-slim

# Définir le dossier de travail
WORKDIR /app

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT=8000
ENV NPM_BIN_PATH=/usr/bin/npm

# Installer les dépendances système + Node.js
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    gnupg \
    libpq-dev \
    python3-dev \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Afficher les versions Node et npm (pour debug)
RUN node -v && npm -v

# Copier les fichiers package.json pour cache Docker
COPY theme/static_src/package*.json /app/theme/static_src/

# Installer les dépendances npm
WORKDIR /app/theme/static_src
RUN npm install

# Revenir au dossier principal
WORKDIR /app

# Copier les dépendances Python
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier tout le projet
COPY . .

# Compiler Tailwind et collecter les fichiers statiques
RUN yes | python manage.py tailwind install \
    && python manage.py tailwind build \
    && python manage.py collectstatic --noinput

# Lancer Gunicorn sur le port Railway ou 8000
CMD gunicorn projetDjango.wsgi:application --bind 0.0.0.0:$PORT
