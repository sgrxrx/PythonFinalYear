from rest_framework import viewsets
from .models import Issue
from .serializers import IssueSerializer

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
        instance.save()