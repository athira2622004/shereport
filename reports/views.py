from django.shortcuts import render


def publications(request):
    return render(request, 'reports/publications.html')
