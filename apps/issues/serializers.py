from django.core.mail import send_mail

from rest_framework import serializers

from .models import Issue

DEPARTMENT_EMAILS = {
    'potholes': 'sauravrijal1011@gmail.com',
    'street_light': 'sunilstha68@gmail.com',
    'water_leakage': 'sunilstha68@gmail.com',
    'garbage': 'sunilstha68@gmail.com',
}

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['reported_by']