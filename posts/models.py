from django.db import models
from django.db.models import QuerySet
# from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from accounts.models import Profile
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator

# Create your models here.

class Food(models.Model):
    title = models.CharField(max_length=20)
    image = models.FileField(upload_to='media/images/', blank=True, null=True)
    pub_date = models.DateTimeField('date published')
    description = models.TextField(max_length=100, null=True, default='', blank=True)
    category = models.CharField(max_length=10, null=True, default='', blank=True)
    category2 = models.CharField(max_length=10, null=True, default='', blank=True)
    price = models.PositiveIntegerField(default=0)
    body = models.TextField()
    address = models.CharField(max_length=100, default='')
    author = models.ForeignKey('accounts.Profile', default=1, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Food', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.text


class Alarm(models.Model):
    message = models.CharField(max_length=100)
    
    