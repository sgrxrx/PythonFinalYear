from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny


from .models import User
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer

class UserRegistrationView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] 

    def get_queryset(self):
        return User.objects.none() 
    
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print("User ID:", self.request.user.id)
        return User.objects.filter(id=self.request.user.id)

    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]  # Allow any user to obtain a token