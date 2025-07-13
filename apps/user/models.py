from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils.text import slugify

from .manager import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=155, null=True)
    email = models.CharField(max_length=55, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_authority = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()