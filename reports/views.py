from django.shortcuts import render
from core.models import CrimeStatistic


def publications(request):
    latest_year = CrimeStatistic.objects.latest('year').year
    return render(request, 'reports/publications.html', {
        'latest_year': latest_year,
    })


def legal_manual_english(request):
    return render(request, 'reports/legal_manual_english.html')


def legal_manual_malayalm(request):
    return render(request, 'reports/legal_manual_malayalm.html')
