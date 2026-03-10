from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SupportRequest


def get_support(request):
    return render(request, 'support/get_support.html')


def reporting_guidance(request):
    return render(request, 'support/reporting_guidance.html')


def legal_literacy(request):
    return render(request, 'support/legal_literacy.html')


def referral_info(request):
    return render(request, 'support/referral_info.html')


def submit_report(request):
    if request.method == 'POST':
        crime_type = request.POST.get('crime_type', '')
        district = request.POST.get('district', '')
        description = request.POST.get('description', '')
        is_anonymous = 'is_anonymous' in request.POST
        name = '' if is_anonymous else request.POST.get('name', '')
        contact = '' if is_anonymous else request.POST.get('contact', '')

        if not crime_type or not description:
            messages.error(
                request, 'Please fill in the crime type and description.')
            return render(request, 'support/submit_report.html')

        try:
            SupportRequest.objects.create(
                crime_type=crime_type,
                district=district,
                description=description,
                is_anonymous=is_anonymous,
                name=name,
                contact=contact,
            )
            messages.success(
                request, 'Your report has been submitted securely. Thank you for your courage.')
        except Exception as e:
            messages.error(
                request, 'There was a problem saving your report. Please try again.')

        return redirect('get_support')

    return render(request, 'support/submit_report.html')
