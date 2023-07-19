from random import choices
from types import ClassMethodDescriptorType
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.
class CustomUser(AbstractUser):
    username=None
    USER_TYPE = (
        ('ADMIN', 'ADMIN'),
        ('CUSTOMER', 'CUSTOMER')
    )

    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    usertype = models.CharField(max_length=255, null=False, blank=False, choices=USER_TYPE, default='CUSTOMER')
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
