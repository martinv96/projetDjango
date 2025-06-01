from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from decimal import Decimal

from .forms import RegisterForm, ProfileForm, ProfileImageForm, SessionForm
from monapp.models import Session


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    sessions = Session.objects.filter(user=request.user)

    total_sessions = sessions.count()
    total_distance = sum((session.distance_km for session in sessions), Decimal('0.0'))
    total_duration = sum((session.duration_minutes for session in sessions), 0)

    # Calcul vitesse moyenne = distance (km) / durée (heures)
    if total_duration > 0:
        duree_heures = Decimal(total_duration) / Decimal('60')
        vitesse_moyenne = round(total_distance / duree_heures, 2)
    else:
        vitesse_moyenne = Decimal('0.0')

    context = {
        'user': request.user,
        'total_sessions': total_sessions,
        'total_distance': float(total_distance),
        'total_duration': total_duration,
        'vitesse_moyenne': float(vitesse_moyenne),
    }

    return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'profile_edit.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def change_profile_photo(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            request.user.profile.photo = image
            request.user.profile.save()
            return redirect('profile')
    else:
        form = ProfileImageForm()
    return render(request, 'monapp/change_photo.html', {'form': form})


@login_required
def create_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return redirect('profile')
    else:
        form = SessionForm()
    return render(request, 'sessions/create_session.html', {'form': form})


@login_required
def session_list(request):
    sessions = Session.objects.filter(user=request.user).order_by('-date')
    return render(request, 'sessions/session_list.html', {'sessions': sessions})
