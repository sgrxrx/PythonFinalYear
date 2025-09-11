from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegistrationView, CustomTokenObtainPairView, UserViewSet, CreateUserWithAuthorityView

app_name = 'user_login'

router = DefaultRouter()
router.register('register', UserRegistrationView, basename='user-register')
router.register('', UserViewSet, basename='user')

urlpatterns =[
    path('login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-authority/', CreateUserWithAuthorityView.as_view({'post': 'create'}), name='create-authority'),
] + router.urls