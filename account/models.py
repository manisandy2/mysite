# src/users/model.py
import datetime
import time

from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password, is_password_usable
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=128)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    gender_detail = [
        ('Male', "Male"),
        ('FeMale', "FeMale")
    ]

    mother_tongue_detail = [
        ('Assamese', 'Assamese'),
        ('Bengali', 'Bengali'),
        ('Gujarati', 'Gujarati'),
        ('Hindi', 'Hindi'),
        ('Kannada', 'Kannada'),
        ('Kashmiri', 'Kashmiri'),
        ('Konkani', 'Konkani'),
        ('Malayalam', 'Malayalam'),
        ('Manipuri', 'Manipuri'),
        ('Marathi', 'Marathi'),
        ('Nepali', 'Nepali'),
        ('Oriya', 'Oriya'),
        ('Punjabi', 'Punjabi'),
        ('Sanskrit', 'Sanskrit'),
        ('Sindhi', 'Sindhi'),
        ('Tamil', 'Tamil'),
        ('Telugu', 'Telugu'),
        ('Urdu', 'Urdu'),
        ('Bodo', 'Bodo'),
        ('Santhali', 'Santhali'),
        ('Maithili', 'Maithili'),
        ('Dogri', 'Dogri'),
    ]

    marital_status_detail = [
        ('New Married', 'New Married'),
        ('Widowed', 'Widowed'),
        ('Divorced', 'Divorced'),
    ]

    Full_Name = models.CharField(max_length=30)
    Gender = models.CharField(choices=gender_detail, max_length=6)
    Marital_Status = models.CharField(choices=marital_status_detail, max_length=300,)
    Mother_Tongue = models.CharField(choices=mother_tongue_detail, max_length=15)
    Mobile_No = models.CharField(max_length=10)

    # date_of_birth = models.CharField(max_length=30)
    # Photo = models.ImageField()
    # Astro_chart = models.ImageField()
    # Height = models.CharField(max_length=30)
    # Complexion = models.CharField(max_length=30)
    # Physical_Status = models.CharField(max_length=30)
    # Body_Type = models.CharField(max_length=30)
    # Educational_Qualification = models.CharField(max_length=30)
    # Employed_In = models.CharField(max_length=30)
    # Occupation = models.CharField(max_length=30)
    # Income = models.CharField(max_length=30)
    #
    # Religious = models.CharField(max_length=30)
    # Caste = models.CharField(max_length=30)
    # Sub_Caste = models.CharField(max_length=30)
    # Gothram = models.CharField(max_length=30)
    # District = models.CharField(max_length=30)
    # Taluk = models.CharField(max_length=30)
    # City = models.CharField(max_length=30)
    # State = models.CharField(max_length=30)
    # Country = models.CharField(max_length=30)

    # def date_of_birth(self):
    #     self.date_of_birth.validate()







