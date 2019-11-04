from django.db import models
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from accounts.models import Profile
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


# # 카트로 넘길 모델 
# class AddtoCart(models.Model):
#     price = models.ForeignKey(Food, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1, null=True)

#     def total_price(self):
#         return self.quantity*price

class Food(models.Model):
    title = models.CharField(max_length=20)
    image = models.FileField(upload_to='images/', blank=True)
    pub_date = models.DateTimeField('date published')
    description = models.TextField(max_length=100, null=True, default='', blank=True)
    category = models.CharField(max_length=10, null=True, default='', blank=True)
    category2 = models.CharField(max_length=10, null=True, default='', blank=True)
    price = models.DecimalField(verbose_name='price', name="price", default=Decimal(0), max_digits=20, decimal_places=0)
    body = models.TextField()
    # body = RichTextUploadingField(blank=True,null=True)
    author = models.ForeignKey(Profile, default=1, on_delete=models.CASCADE)
#    verbose_name='price'
#  user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:30]

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    # 카카오톡 아이디로 변경해야함
    # settings.AUTH_USER_MODEL 
    post = models.ForeignKey('food.Food', related_name='comments', on_delete = models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text



