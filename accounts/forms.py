from django import forms 
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model
from .models import Profile

# class ProfileForm(forms.ModelForm):
#     profile_photo = forms.ImageField(required=False)
#     class Meta:
#         model = Profile
#         # fields = '__all__'
#         fields = ('nickname', 'profile_photo', 'address', 'bizNumber', )
