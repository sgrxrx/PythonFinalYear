from django.core.mail import EmailMessage

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Issue, Authority
from .serializers import IssueSerializer
from apps.issues.ml_utils import predict_issue_type


DEPARTMENT_EMAILS = {
    'potholes': 'sauravrijal1011@gmail.com',
    'street_light': 'sunilstha68@gmail.com',
    'water_leakage': 'sunilstha68@gmail.com',
    'garbage': 'sunilstha68@gmail.com',
}

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    # def get_queryset(self):
    #     queryset = Issue.objects.all()
    #     status = self.request.query_params.get('status')
    #     user_specific = self.request.query_params.get('user_specific')

    #     if status:
    #         queryset = queryset.filter(status=status)
    #     if user_specific == 'true':
    #         queryset = queryset.filter(reported_by=self.request.user)
    #     return queryset
    def get_queryset(self):
        queryset = Issue.objects.all()
        status = self.request.query_params.get('status')
        user_specific = self.request.query_params.get('user_specific')

        if status:
            queryset = queryset.filter(status=status)

        if user_specific == 'true':
            # Check if current user is an authority
            authority = Authority.objects.filter(user=self.request.user).first()
            if authority and authority.issue_type:
                # User is an authority, return issues of their type
                queryset = queryset.filter(issue_type=authority.issue_type)
            else:
                # User is not an authority, return issues reported by them
                queryset = queryset.filter(reported_by=self.request.user)

        return queryset


    def perform_create(self, serializer):
        instance = serializer.save(reported_by=self.request.user)
        if instance.image:
            predicted_type = predict_issue_type(instance.image.path)
            instance.issue_type = predicted_type
            instance.save()