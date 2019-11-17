from django.contrib import admin
from .models import *
from decimal import Decimal

# Register your models here.
admin.site.register(Food)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(Cart2)

