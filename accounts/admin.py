from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Register your models here.

class Profileline(admin.StackedInline):
    model = Profile
    con_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (Profileline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
