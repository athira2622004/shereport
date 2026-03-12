from django.shortcuts import render
from core.models import CrimeStatistic


def publications(request):
    latest_year = CrimeStatistic.objects.latest('year').year
    return render(request, 'reports/publications.html', {
        'latest_year': latest_year,
    })
