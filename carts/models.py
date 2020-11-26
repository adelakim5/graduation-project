from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import Profile
from posts.models import *
from django import forms

# Create your models here.
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

class CustomerForm(forms.ModelForm):
    REASON=[
        ('no-show', '노쇼'),
        ('accept', '승인'),
        ('cancel', '취소'),
        ('etc', '기타')
    ]
    reason = forms.ChoiceField(widget = forms.RadioSelect, choices=REASON, initial='accept', required=True)
    others = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '집중 고객으로 등록하려는 이유를 자세히 적어주세요.'}))
    
    class Meta:
        model = Customer
        fields = ('reason', 'others')
