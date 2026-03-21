from django.shortcuts import render
from .models import PolicyUpdate


def policy(request):
    category = request.GET.get('category', 'all')
    updates = PolicyUpdate.objects.filter(is_active=True)
    if category != 'all':
        updates = updates.filter(category=category)
    return render(request, 'policy/policy.html', {
        'updates':          updates,
        'selected_category': category,
        'categories':       PolicyUpdate.CATEGORY_CHOICES,
    })


def rti_resources(request):
    return render(request, 'policy/rti_resources.html')
