from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.user.models import User  # adjust path if needed

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims here
        token['name'] = user.name
        token['email'] = user.email
        return token

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise Exception("Invalid credentials")
        except User.DoesNotExist:
            raise Exception("User not found")

        # manually attach user for token creation
        data = super().validate({
            'username': email,  # This field is required but we override it
            'password': password
        })
        self.user = user
        return data
