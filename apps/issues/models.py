from django.db import models
from django.contrib.auth import get_user_model

class Issue(models.Model):
    ISSUE_TYPE_CHOICES = [
        ('Potholes', 'Potholes'),
        ('Street Light', 'Street Light'),
        ('Water Leakage', 'Water Leakage'),
        ('Garbage', 'Garbage'),
        ('Not Labelled', 'Not Labelled'),
    ]    

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
        ('Verifying', 'Verifying'),
        ('Accepted', 'Accepted'),
        ('Assigned to Authority', 'Assigned to Authority'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPE_CHOICES, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    image = models.ImageField(upload_to='issues/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Low')
    assigned_to = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    authority_comment = models.TextField(null=True, blank=True)
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reported_issues')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.issue_type
    
class Authority(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='authority_profile')
    issue_type = models.CharField(max_length=50, choices=Issue.ISSUE_TYPE_CHOICES, blank=True, null=True)

    # def __str__(self):
    #     return self.user