from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=60, null=True)
    profile_photo = models.ImageField(blank=True)
    address = models.CharField(max_length=60, null=True)
    bizNumber = models.CharField(max_length=60, null=True)
  
    def __str__(self):
        return self.nickname
# Create your models here.
