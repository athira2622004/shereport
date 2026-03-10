from django.db import models


class ContactMessage(models.Model):
    PURPOSE_CHOICES = [
        ('partnership', 'Partnership / Collaboration'),
        ('academic',    'Academic Research'),
        ('media',       'Media Inquiry'),
        ('ngo',         'NGO / Civil Society'),
        ('feedback',    'Feedback'),
        ('general',     'General Inquiry'),
    ]
    name         = models.CharField(max_length=200)
    email        = models.EmailField()
    organisation = models.CharField(max_length=200, blank=True)
    purpose      = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    message      = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)
    is_read      = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.get_purpose_display()} ({self.created_at.date()})"
