from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate

from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class UserRegistrationView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def get_queryset(self):
        return User.objects.none() 