from django.db import models


class PolicyUpdate(models.Model):
    CATEGORY_CHOICES = [
        ('new_law',        'New Law'),
        ('court_ruling',   'Court Ruling'),
        ('policy_gap',     'Policy Gap'),
        ('recommendation', 'Recommendation'),
        ('law_update',     'Law Update'),
    ]

    title = models.CharField(max_length=300)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField()
    description = models.TextField()
    source = models.CharField(
        max_length=300, blank=True, help_text='Source URL or reference')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"
