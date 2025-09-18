from django.core.mail import EmailMessage

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Issue, Authority
from .serializers import IssueSerializer
from apps.issues.ml_utils import predict_issue_type

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all()
        status = self.request.query_params.get('status')
        user_specific = self.request.query_params.get('user_specific')

        # If user is staff, return all issues (optionally filter by status)
        if self.request.user.is_staff:
            if status:
                return queryset.filter(status=status)
            return queryset

        authority = Authority.objects.filter(user=self.request.user).first()

        # Only filter for authority/status on list view
        if self.action == 'list':
            if authority and authority.issue_type:
                return queryset.filter(issue_type=authority.issue_type, status='Assigned to Authority')
            if status:
                queryset = queryset.filter(status=status)
            if user_specific == 'true':
                if authority and authority.issue_type:
                    queryset = queryset.filter(issue_type=authority.issue_type, status='Assigned to Authority')
                else:
                    queryset = queryset.filter(reported_by=self.request.user)
            elif not status and not user_specific:
                if authority and authority.issue_type:
                    queryset = queryset.filter(issue_type=authority.issue_type, status='Assigned to Authority')
                else:
                    queryset = queryset.filter(reported_by=self.request.user)
            return queryset

        # For detail views, allow access to all issues (or add your own permission logic)
        return queryset


    def perform_create(self, serializer):
        from apps.issues.ml_utils import map_ml_label_to_django
        instance = serializer.save(reported_by=self.request.user)
        if instance.image and hasattr(instance.image, 'path'):
            print("Image path:", instance.image.path)
            predicted_type = predict_issue_type(instance.image.path)
            print(f"Predicted issue type: {predicted_type}")
            instance.issue_type = map_ml_label_to_django(predicted_type)
        else:
            print("No image uploaded.")
            instance.issue_type = "Not Labelled"
        instance.save()