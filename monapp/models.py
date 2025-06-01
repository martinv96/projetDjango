from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    duration_minutes = models.PositiveIntegerField()
    parcours_nom = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def vitesse_moyenne(self):
        if self.duration_minutes == 0:
            return 0
        return round(float(self.distance_km) / (self.duration_minutes / 60), 2)