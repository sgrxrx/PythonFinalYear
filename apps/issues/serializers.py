from django.core.mail import send_mail

from rest_framework import serializers

from .models import Issue

DEPARTMENT_EMAILS = {
    'Potholes': 'sauravrijal1011@gmail.com',
    'Street Light': 'sunilstha68@gmail.com',
    'Water Leakage': 'sunilstha68@gmail.com',
    'Garbage': 'sunilstha68@gmail.com',
}

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['reported_by']