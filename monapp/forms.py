from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from monapp.models import Profile, Session

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_("E-mail"))

    password1 = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=forms.PasswordInput,
        help_text="",
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': _("Nom d'utilisateur"),
            'password2': _("Confirmation du mot de passe"),
        }
        help_texts = {
            'username': _("Requis. 150 caractères ou moins. Lettres, chiffres et @/./+/-/_ seulement."),
            'password2': _("Entrez le même mot de passe que précédemment, pour vérification."),
        }

class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'rounded border px-3 py-2 w-full'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'rounded border px-3 py-2 w-full'})
    )

    class Meta:
        model = Profile
        fields = ['photo']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile

# Nouveau formulaire pour mettre à jour uniquement la photo de profil
class ProfileImageForm(forms.Form):
    image = forms.ImageField(required=True)

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date', 'distance_km', 'duration_minutes', 'parcours_nom']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }