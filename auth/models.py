from django.db import models
from django.contrib.auth.models import  BaseUserManager
import uuid
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db.models.fields import EmailField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db.models import Q
from django.utils import timezone

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_('The Email must be set'))
        extra_fields.setdefault('is_verified', True)
        email = self.normalize_email(email)         
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return email

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex], blank = True, null=True)  # you can set it unique = True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyAccountManager()

    def __str__(self):
        return self.email