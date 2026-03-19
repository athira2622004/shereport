from django.db import models


class SupportRequest(models.Model):
    CRIME_TYPES = [
        ('domestic_violence', 'Domestic Violence / Cruelty by Husband'),
        ('rape', 'Rape / Sexual Assault'),
        ('molestation', 'Molestation / Sexual Harassment'),
        ('stalking', 'Stalking / Cyberstalking'),
        ('kidnapping', 'Kidnapping'),
        ('dowry', 'Dowry Harassment / Dowry Death'),
        ('trafficking', 'Human Trafficking'),
        ('workplace', 'Workplace Harassment'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('referred', 'Referred'),
        ('closed', 'Closed'),
    ]

    crime_type = models.CharField(max_length=50, choices=CRIME_TYPES)
    district = models.CharField(max_length=100, blank=True)
    incident_date = models.DateField(null=True, blank=True)
    incident_time = models.TimeField(null=True, blank=True)
    institution = models.CharField(max_length=300, blank=True)
    reported_to_police = models.BooleanField(default=False)
    needs_legal_help = models.BooleanField(default=False)
    evidence_file = models.FileField(
        upload_to='evidence/', blank=True, null=True)
    # What help do you need
    help_filing_complaint = models.BooleanField(default=False)
    help_legal_support = models.BooleanField(default=False)
    help_court_support = models.BooleanField(default=False)
    help_recovery = models.BooleanField(default=False)
    help_safety_planning = models.BooleanField(default=False)
    help_ngo_referral = models.BooleanField(default=False)
    help_other = models.BooleanField(default=False)
    help_other_text = models.TextField(blank=True)
    description = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    name = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        tag = 'Anonymous' if self.is_anonymous else self.name
        return f"[{self.get_crime_type_display()}] {tag} — {self.created_at.date()}"
