from django.shortcuts import render

def home(request):
    return render(request, 'base.html')  # home.html est ton template avec Tailwind
