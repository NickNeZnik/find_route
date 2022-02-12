
from django.shortcuts import render


def home(request):

    name = 'Bobby'
    return render(request, 'home.html', {'name': name})
