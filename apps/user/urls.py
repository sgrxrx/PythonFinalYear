from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegistrationView, CustomTokenObtainPairView, UserViewSet

app_name = 'user_login'

router = DefaultRouter()
router.register('register', UserRegistrationView, basename='user-register')
router.register('', UserViewSet, basename='user')
urlpatterns = router.urls + [
    path('login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]