from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=60, null=True)
    address = models.CharField(max_length=60, null=True)
    bizNumber = models.CharField(max_length=60, null=True)
    
    class Meta:
        permissions = [
            ("profile_status", "Can register the posts and customers, also decide the status of requests")
        ]
  
    def __str__(self):
        return self.nickname
# Create your models here.
