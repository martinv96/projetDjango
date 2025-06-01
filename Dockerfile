FROM python:3.13-slim

WORKDIR /app

# Installer Node.js et npm
RUN apt-get update && apt-get install -y nodejs npm

COPY package.json package-lock.json* /app/
RUN npm install

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

# Build Tailwind CSS et collecter static files
RUN python manage.py tailwind build && python manage.py collectstatic --noinput

CMD ["gunicorn", "projetDjango.wsgi:application"]
