from django.shortcuts import render


def policy(request):
    return render(request, 'policy/policy.html')


def rti_resources(request):
    return render(request, 'policy/rti_resources.html')
