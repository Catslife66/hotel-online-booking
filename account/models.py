from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    #user_session_key = models.CharField(max_length=40, blank=True, null=True)
    pass