
from django.db import models
from django.db.models import QuerySet
from accounts.models import Profile
from django.conf import settings

class Notification(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)