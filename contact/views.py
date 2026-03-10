from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage


def contact(request):
    if request.method == 'POST':
        name     = request.POST.get('name', '')
        email    = request.POST.get('email', '')
        org      = request.POST.get('organisation', '')
        purpose  = request.POST.get('purpose', '')
        message  = request.POST.get('message', '')
        ContactMessage.objects.create(
            name=name, email=email, organisation=org,
            purpose=purpose, message=message
        )
        messages.success(request, 'Thank you for reaching out! We will get back to you within 3 working days.')
        return redirect('contact')
    return render(request, 'contact/contact.html')
