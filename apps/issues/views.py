from django.core.mail import EmailMessage

from rest_framework import viewsets

from .models import Issue
from .serializers import IssueSerializer


DEPARTMENT_EMAILS = {
    'potholes': 'sauravrijal1011@gmail.com',
    'street_light': 'sunilstha68@gmail.com',
    'water_leakage': 'sunilstha68@gmail.com',
    'garbage': 'sunilstha68@gmail.com',
}

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        status = self.request.query_params.get('status')
        user_specific = self.request.query_params.get('user_specific')

        if status:
            queryset = queryset.filter(status=status)
        if user_specific == 'true':
            queryset = queryset.filter(reported_by=self.request.user)
        return queryset


    def perform_create(self, serializer):
        instance = serializer.save(reported_by=self.request.user)
        department_email = DEPARTMENT_EMAILS.get(instance.issue_type)
        print(f"Department email for {instance.issue_type}: {department_email}")
        if department_email:
            # Create a Google Maps link
            maps_link = f"https://www.google.com/maps/search/?api=1&query={instance.latitude},{instance.longitude}"
            message = (
                f"Issue Description: {instance.description}\n"
                f"Map: {maps_link}"
            )
            email = EmailMessage(
                subject=f"New Issue Reported: {instance.get_issue_type_display()}",
                body=message,
                from_email=None,  # Uses DEFAULT_FROM_EMAIL
                to=[department_email],
            )
            # Attach image if present
            if instance.image:
                email.attach_file(instance.image.path)
            email.send(fail_silently=False)