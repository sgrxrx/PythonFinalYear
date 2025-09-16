
from django.db.models.signals import post_save
from django.dispatch import receiver

DEPARTMENT_EMAILS = {
    'Potholes': 'sauravrijal1011@gmail.com',
    'Street Light': 'sunilstha68@gmail.com',
    'Water Leakage': 'sunilstha68@gmail.com',
    'Garbage': 'sunilstha68@gmail.com',
}


# Delay model and DEPARTMENT_EMAILS import until signal is called
@receiver(post_save, sender=None)
def send_issue_status_email(sender, instance, created, **kwargs):
    from apps.issues.models import Issue
    if sender is not Issue:
        return
    if not created:
        if instance.status == 'Accepted':
            from django.core.mail import EmailMessage
            department_email = DEPARTMENT_EMAILS.get(instance.issue_type)
            if department_email:
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
                if instance.image:
                    email.attach_file(instance.image.path)
                email.send(fail_silently=False)
                # Change status to Assigned to Authority and save
                instance.status = 'Assigned to Authority'
                instance.save(update_fields=['status'])
