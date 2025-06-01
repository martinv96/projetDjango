FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y nodejs npm

# Copier package.json et package-lock.json pour npm install
COPY theme/static_src/package.json theme/static_src/package-lock.json* /app/

RUN npm install

# Copier requirements et installer les dépendances python
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copier le reste de l'application
COPY . /app/

# Construire tailwind et collecter les fichiers statiques Django
RUN python manage.py tailwind build && python manage.py collectstatic --noinput

# Démarrer l'application avec gunicorn
CMD ["gunicorn", "projetDjango.wsgi:application"]
