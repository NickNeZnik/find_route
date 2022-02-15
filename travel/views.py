
from django.shortcuts import render


def home(request):

    name = 'Bobby'
    return render(request, 'home.html', {'name': name})

def about(request):

    name = 'About page'
    return render(request, 'about.html', {'name': name})
