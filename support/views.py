from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
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
        incident_date = request.POST.get('incident_date') or None
        incident_time = request.POST.get('incident_time') or None
        institution = request.POST.get('institution', '')
        reported_to_police = 'reported_to_police' in request.POST
        needs_legal_help = 'needs_legal_help' in request.POST
        evidence_file = request.FILES.get('evidence_file')
        help_filing_complaint = 'help_filing_complaint' in request.POST
        help_legal_support = 'help_legal_support' in request.POST
        help_court_support = 'help_court_support' in request.POST
        help_recovery = 'help_recovery' in request.POST
        help_safety_planning = 'help_safety_planning' in request.POST
        help_ngo_referral = 'help_ngo_referral' in request.POST
        help_other = 'help_other' in request.POST
        help_other_text = request.POST.get('help_other_text', '')

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
                incident_date=incident_date,
                incident_time=incident_time,
                institution=institution,
                reported_to_police=reported_to_police,
                needs_legal_help=needs_legal_help,
                evidence_file=evidence_file,
                help_filing_complaint=help_filing_complaint,
                help_legal_support=help_legal_support,
                help_court_support=help_court_support,
                help_recovery=help_recovery,
                help_safety_planning=help_safety_planning,
                help_ngo_referral=help_ngo_referral,
                help_other=help_other,
                help_other_text=help_other_text,
            )

            # Send email notification to admin
            try:
                identity = "Anonymous submission" if is_anonymous else f"Name: {name}\nContact: {contact}"
                send_mail(
                    subject=f'New Support Request — SHE Report ({crime_type})',
                    message=f"""A new support request has been submitted on SHE Report.

Crime Type  : {crime_type}
District    : {district or 'Not specified'}
Anonymous   : {'Yes' if is_anonymous else 'No'}
{identity}

Description:
{description}

---
View in admin: http://127.0.0.1:8000/admin/support/supportrequest/
""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request, 'Your report has been submitted securely. Thank you for your courage.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

        return redirect('get_support')

    return render(request, 'support/submit_report.html')
