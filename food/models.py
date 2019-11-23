from django.db import models
from django.db.models import QuerySet
# from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from accounts.models import Profile
# from ckeditor.fields import RichTextField
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
    author = models.ForeignKey('accounts.Profile', default=1, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    post = models.ForeignKey('food.Food', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.text

class Cart(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    # sender는 카카오톡 api로 바꿔줘야함
    receiver = models.ForeignKey('accounts.Profile', default=1, on_delete=models.CASCADE)
    people = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    request_date = models.DateTimeField(default=timezone.now)
    title = models.ForeignKey(Food, default=1, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

class Cart2(models.Model):
    STATUS = (
        ('-1', 'failed'),
        ('0', 'pending'),
        ('1', 'approved'),
    )
    tid = models.CharField(max_length=30, primary_key=True, default='default')
    order_id = models.PositiveIntegerField(default=0)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    # sender는 카카오톡 api로 바꿔줘야함
    receiver = models.ForeignKey('accounts.Profile', default=1, on_delete=models.CASCADE)
    people = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    request_date = models.DateTimeField(default=timezone.now)
    title = models.ForeignKey(Food, default=1, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUS, default='0')
    phone = models.CharField(max_length=20)
    
class Cart3(models.Model):
    order_id = models.PositiveIntegerField(default=0)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    receiver = models.ForeignKey('accounts.Profile', default=1, on_delete=models.CASCADE)
    people = models.PositiveIntegerField(default=0)
    total_price = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    title = models.ForeignKey(Food, default=1, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, default='0')
    
class Customer(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    whose = models.ForeignKey('accounts.Profile', default=1, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    others = models.TextField()
    # comments가 갯수 세어진것처럼 
    
class Alarm(models.Model):
    message = models.CharField(max_length=100)
    
    