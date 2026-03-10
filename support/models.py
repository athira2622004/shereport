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

    crime_type   = models.CharField(max_length=50, choices=CRIME_TYPES)
    district     = models.CharField(max_length=100, blank=True)
    description  = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    name         = models.CharField(max_length=200, blank=True)
    contact      = models.CharField(max_length=100, blank=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at   = models.DateTimeField(auto_now_add=True)
    notes        = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        tag = 'Anonymous' if self.is_anonymous else self.name
        return f"[{self.get_crime_type_display()}] {tag} — {self.created_at.date()}"
