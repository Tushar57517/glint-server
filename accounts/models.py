from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    pronouns = models.CharField(max_length=20, blank=True, null=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.username