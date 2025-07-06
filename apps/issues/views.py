from rest_framework import viewsets
from .models import Issue
from .serializers import IssueSerializer

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        instance = serializer.save(reported_by=self.request.user)
        instance.save()