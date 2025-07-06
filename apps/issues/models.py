from django.db import models
from django.contrib.auth import get_user_model

class Issue(models.Model):
    ISSUE_TYPE_CHOICES = [
        ('potholes', 'Potholes'),
        ('traffic_light', 'Traffic Light'),
        ('street_light', 'Street Light'),
        ('water_leakage', 'Water Leakage'),
        ('garbage', 'Garbage'),
    ]    

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In_progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]


    description = models.TextField()
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPE_CHOICES)
    latitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    image = models.ImageField(upload_to='issues/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reported_issues')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title