"""
URL configuration for projetDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from monapp.views import login_view
from django.conf import settings
from django.conf.urls.static import static
from monapp import views  # Assurez-vous d'importer les vues de votre application monapp
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Assurez-vous d'importer la vue home depuis theme.views
    path('register/', views.register, name='register'),  # Remplacez par la vue d'enregistrement appropriée
    path('login/', login_view, name='login'),  # Remplacez par la vue de connexion appropriée
    path('logout/', views.logout_view, name='logout'),  # Remplacez par la vue de déconnexion appropriée
    path('profile/', views.profile, name='profile'),  # Remplacez par la vue de profil appropriée
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # Remplacez par la vue d'édition de profil appropriée
    path('password/change/', views.change_password, name='change_password'),  # Remplacez par la vue de changement de mot de passe appropriée
    path('profile/photo/', views.change_profile_photo, name='change_profile_photo'),
     path('sessions/new/', views.create_session, name='create_session'),
    path('sessions/', views.session_list, name='session_list'),
     # Mot de passe oublié
    path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),

    path('mot-de-passe-oublie/envoye/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reinitialisation/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reinitialisation/terminee/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)