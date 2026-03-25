from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import LawyerVolunteer, LawyerConnectionRequest, StudentVolunteer, StudentConnectionRequest


def lawyer_list(request):
    """Show approved lawyers and students — survivors can request connection."""
    district = request.GET.get('district', '')
    specialization = request.GET.get('specialization', '')

    lawyers = LawyerVolunteer.objects.filter(is_approved=True)
    students = StudentVolunteer.objects.filter(is_approved=True)

    if district:
        lawyers = lawyers.filter(district=district)
        students = students.filter(district=district)
    if specialization:
        lawyers = lawyers.filter(specialization=specialization)
        # students don't have specialization, so skip that filter for them

    districts = LawyerVolunteer.DISTRICT_CHOICES
    specializations = LawyerVolunteer.SPECIALIZATION_CHOICES

    return render(request, 'volunteers/lawyer_list.html', {
        'lawyers':           lawyers,
        'students':          students,
        'districts':         districts,
        'specializations':   specializations,
        'selected_district': district,
        'selected_spec':     specialization,
    })


def connect_lawyer(request, pk):
    """Survivor requests connection with a specific lawyer."""
    lawyer = get_object_or_404(LawyerVolunteer, pk=pk, is_approved=True)

    if request.method == 'POST':
        is_anonymous = 'is_anonymous' in request.POST
        survivor_name = '' if is_anonymous else request.POST.get(
            'survivor_name', '')
        contact = '' if is_anonymous else request.POST.get('contact', '')
        message = request.POST.get('message', '')

        LawyerConnectionRequest.objects.create(
            lawyer=lawyer,
            survivor_name=survivor_name,
            contact=contact,
            message=message,
            is_anonymous=is_anonymous,
        )
        messages.success(
            request, 'Your request has been sent. Our team will contact you shortly to make the connection.')
        return redirect('lawyer_list')

    return render(request, 'volunteers/connect_lawyer.html', {'lawyer': lawyer})


def connect_student(request, pk):
    """Survivor requests connection with a specific LLB student volunteer."""
    student = get_object_or_404(StudentVolunteer, pk=pk, is_approved=True)

    if request.method == 'POST':
        is_anonymous = 'is_anonymous' in request.POST
        survivor_name = '' if is_anonymous else request.POST.get(
            'survivor_name', '')
        contact = '' if is_anonymous else request.POST.get('contact', '')
        message = request.POST.get('message', '')

        StudentConnectionRequest.objects.create(
            student=student,
            survivor_name=survivor_name,
            contact=contact,
            message=message,
            is_anonymous=is_anonymous,
        )
        messages.success(
            request, 'Your request has been sent. Our team will contact you shortly to make the connection.')
        return redirect('lawyer_list')

    return render(request, 'volunteers/connect_student.html', {'student': student})


def register_lawyer(request):
    """Lawyers register themselves as volunteers."""
    if request.method == 'POST':
        try:
            LawyerVolunteer.objects.create(
                name=request.POST.get('name', ''),
                specialization=request.POST.get('specialization', ''),
                district=request.POST.get('district', ''),
                languages=request.POST.get('languages', ''),
                experience_years=int(request.POST.get(
                    'experience_years', 0) or 0),
                bar_council_no=request.POST.get('bar_council_no', ''),
                email=request.POST.get('email', ''),
                phone=request.POST.get('phone', ''),
                pro_bono='pro_bono' in request.POST,
                reduced_cost='reduced_cost' in request.POST,
                availability=request.POST.get('availability', ''),
                bio=request.POST.get('bio', ''),
                is_approved=False,
            )
            messages.success(
                request, 'Thank you for registering! Your profile will be reviewed and approved shortly.')
            return redirect('register_lawyer')
        except Exception:
            messages.error(
                request, 'There was a problem submitting your registration. Please try again.')

    return render(request, 'volunteers/register_lawyer.html')


def register_student(request):
    """LLB students register themselves as volunteers."""
    if request.method == 'POST':
        try:
            StudentVolunteer.objects.create(
                name=request.POST.get('name', ''),
                college=request.POST.get('college', ''),
                year_of_study=int(request.POST.get('year_of_study', 1) or 1),
                district=request.POST.get('district', ''),
                languages=request.POST.get('languages', ''),
                is_supervised='is_supervised' in request.POST,
                legal_awareness=True,
                document_assistance='document_assistance' in request.POST,
                email=request.POST.get('email', ''),
                phone=request.POST.get('phone', ''),
                bio=request.POST.get('bio', ''),
                is_approved=False,
            )
            messages.success(
                request, 'Thank you for registering! Your profile will be reviewed and approved shortly.')
            return redirect('register_student')
        except Exception:
            messages.error(
                request, 'There was a problem submitting your registration. Please try again.')

    return render(request, 'volunteers/register_student.html')
