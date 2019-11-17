from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

# @receiver(post_save, sender=Cart2)
# def cart2_post_save(sender, **kwargs):
#     cart = kwargs['instance'].order_id
#     obj = Cart.objects.get(id=cart)
#     if obj is not None:
#         Cart.objects.get(id=cart).delete()

    