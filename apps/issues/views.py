from django.core.mail import EmailMessage

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Issue, Authority
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
        authority = Authority.objects.filter(issue_type=instance.issue_type).first()
        if authority:
            instance.assigned_to = authority.user
            instance.save()
        
       
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_status = instance.status
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        # Check if status changed to "Accepted" (or "Approved" if you rename)
        if old_status != updated_instance.status and updated_instance.status.lower() == "accepted":
            department_email = DEPARTMENT_EMAILS.get(updated_instance.issue_type)
            if department_email:
                maps_link = f"https://www.google.com/maps/search/?api=1&query={updated_instance.latitude},{updated_instance.longitude}"
                message = (
                    f"Issue '{updated_instance.title}' has been approved!\n"
                    f"Issue Description: {updated_instance.description}\n"
                    f"Map: {maps_link}"
                )
                email = EmailMessage(
                    subject=f"Issue Approved: {updated_instance.get_issue_type_display()}",
                    body=message,
                    from_email=None,
                    to=[department_email],
                )
                if updated_instance.image:
                    email.attach_file(updated_instance.image.path)
                email.send(fail_silently=False)
                updated_instance.status = "Assigned to Authority"
                updated_instance.save(update_fields=["status"])
                

        serializer = self.get_serializer(updated_instance)
        return Response(serializer.data)