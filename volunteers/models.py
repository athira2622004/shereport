from django.db import models


class LawyerVolunteer(models.Model):
    SPECIALIZATION_CHOICES = [
        ('domestic_violence', 'Domestic Violence / DV Act'),
        ('sexual_offences',   'Sexual Offences / POCSO'),
        ('family_law',        'Family Law'),
        ('criminal_law',      'Criminal Law'),
        ('human_rights',      'Human Rights'),
        ('labour_law',        'Labour / Workplace Harassment'),
        ('general',           'General Practice'),
        ('other',             'Other'),
    ]
    DISTRICT_CHOICES = [
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('Kollam',             'Kollam'),
        ('Pathanamthitta',     'Pathanamthitta'),
        ('Alappuzha',          'Alappuzha'),
        ('Kottayam',           'Kottayam'),
        ('Idukki',             'Idukki'),
        ('Ernakulam',          'Ernakulam'),
        ('Thrissur',           'Thrissur'),
        ('Palakkad',           'Palakkad'),
        ('Malappuram',         'Malappuram'),
        ('Kozhikode',          'Kozhikode'),
        ('Wayanad',            'Wayanad'),
        ('Kannur',             'Kannur'),
        ('Kasaragod',          'Kasaragod'),
    ]

    name = models.CharField(max_length=200)
    specialization = models.CharField(
        max_length=50, choices=SPECIALIZATION_CHOICES)
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
    languages = models.CharField(
        max_length=200, help_text='e.g. Malayalam, English, Hindi')
    experience_years = models.IntegerField(
        default=0, help_text='Years of experience')
    bar_council_no = models.CharField(
        max_length=100, blank=True, help_text='Bar Council registration number')

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    pro_bono = models.BooleanField(
        default=False, help_text='Available for free pro-bono work')
    reduced_cost = models.BooleanField(
        default=False, help_text='Available for reduced-cost work')
    availability = models.CharField(
        max_length=300, blank=True, help_text='e.g. Weekends, evenings, full-time')

    bio = models.TextField(
        blank=True, help_text='Brief description of your experience and how you can help')

    is_approved = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text='Admin notes')

    class Meta:
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.name} — {self.get_specialization_display()} ({self.district})"


class StudentVolunteer(models.Model):
    YEAR_CHOICES = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
        (5, '5th Year'),
    ]
    DISTRICT_CHOICES = LawyerVolunteer.DISTRICT_CHOICES

    name = models.CharField(max_length=200)
    college = models.CharField(
        max_length=300, help_text='College / University name')
    year_of_study = models.IntegerField(
        choices=YEAR_CHOICES, help_text='Current year of LLB')
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
    languages = models.CharField(
        max_length=200, help_text='e.g. Malayalam, English')
    is_supervised = models.BooleanField(
        default=False, help_text='Supervised by a registered advocate')

    # Offerings (fixed for students)
    legal_awareness = models.BooleanField(
        default=True, help_text='Offers legal awareness / guidance')
    document_assistance = models.BooleanField(
        default=False, help_text='Offers document assistance')

    email = models.EmailField()
    phone = models.CharField(max_length=20)

    bio = models.TextField(blank=True)

    is_approved = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text='Admin notes')

    class Meta:
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.name} — LLB Year {self.year_of_study} ({self.district})"


class LawyerConnectionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('connected', 'Connected'),
        ('closed',    'Closed'),
    ]
    lawyer = models.ForeignKey(
        LawyerVolunteer, on_delete=models.CASCADE, related_name='connection_requests')
    survivor_name = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        tag = 'Anonymous' if self.is_anonymous else self.survivor_name
        return f"Request for {self.lawyer.name} from {tag}"


class StudentConnectionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('connected', 'Connected'),
        ('closed',    'Closed'),
    ]
    student = models.ForeignKey(
        StudentVolunteer, on_delete=models.CASCADE, related_name='connection_requests')
    survivor_name = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        tag = 'Anonymous' if self.is_anonymous else self.survivor_name
        return f"Request for {self.student.name} from {tag}"
