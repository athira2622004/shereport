from django.db import models


class CrimeStatistic(models.Model):
    """Year-wise crime statistics for Kerala."""
    year = models.IntegerField()
    total_crimes = models.IntegerField()
    rape = models.IntegerField(default=0)
    molestation = models.IntegerField(default=0)
    kidnapping = models.IntegerField(default=0)
    cruelty_by_husband = models.IntegerField(default=0)
    dowry_deaths = models.IntegerField(default=0)
    harassment = models.IntegerField(default=0)
    other = models.IntegerField(default=0)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['year']

    def __str__(self):
        return f"Crime Stats {self.year}"


class DistrictData(models.Model):
    """District-wise crime data."""
    DISTRICT_CHOICES = [
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('Kollam', 'Kollam'),
        ('Pathanamthitta', 'Pathanamthitta'),
        ('Alappuzha', 'Alappuzha'),
        ('Kottayam', 'Kottayam'),
        ('Idukki', 'Idukki'),
        ('Ernakulam', 'Ernakulam'),
        ('Thrissur', 'Thrissur'),
        ('Palakkad', 'Palakkad'),
        ('Malappuram', 'Malappuram'),
        ('Kozhikode', 'Kozhikode'),
        ('Wayanad', 'Wayanad'),
        ('Kannur', 'Kannur'),
        ('Kasaragod', 'Kasaragod'),
    ]
    district = models.CharField(max_length=100, choices=DISTRICT_CHOICES)
    year = models.IntegerField()
    total_crimes = models.IntegerField(null=True, blank=True)
    rape = models.IntegerField(null=True, blank=True)
    molestation = models.IntegerField(null=True, blank=True)
    kidnapping = models.IntegerField(null=True, blank=True)
    cruelty_by_husband = models.IntegerField(null=True, blank=True)
    dowry_deaths = models.IntegerField(null=True, blank=True)
    harassment = models.IntegerField(null=True, blank=True)
    other = models.IntegerField(null=True, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['year', 'district']

    def __str__(self):
        return f"{self.district} - {self.year}"


class NewsUpdate(models.Model):
    """Latest news and updates shown on homepage."""
    title = models.CharField(max_length=300)
    summary = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    source = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    date_published = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_published']

    def __str__(self):
        return self.title
