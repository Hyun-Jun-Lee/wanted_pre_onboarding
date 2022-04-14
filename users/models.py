from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = ((GENDER_MALE, "Male"), (GENDER_FEMALE, "Female"))
    
    username = models.CharField(max_length=30, unique=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, blank=True
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    