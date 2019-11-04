from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model
from .models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=False, max_length=60)
    address = forms.CharField(required=True)
    bizNumber = forms.CharField(required=True)
    # nickname = forms.CharField(required=True)

    # first_name = forms.CharField(max_length=100, label="이름", widget=forms.TextInput(attrs={
    #     'placeholder':'First name',
    # }))
    # last_name = forms.CharField(max_length=100, label="성", widget=forms.TextInput(attrs={
    #     'placeholder':'Last name',
    # }))
    # username = forms.RegexField(label="아이디", max_length=30, regex=r'^[\w.@+-]+$', help_text="Required. 30 characters or fewer. Letters, digits and " "@/./+/-/_ only.",
    # error_messages = {
    #     'invalid': "This value may contain only letters, numbers, and" "@/./+/-/_ characters."
    # },
    # widget = forms.TextInput(attrs={
    #     'placeholder': 'Username',
    #     'required': 'true',
    # }))
    # email = forms.EmailField(
    #     required=False,
    #     widget=forms.EmailInput(attrs={
    #         'placeholder':'your@email.com',
    #         'required': 'false'
    #     }),
    #     max_length=200)
    # password1 = forms.CharField(label="비밀번호", 
    #     widget=forms.PasswordInput(attrs={
    #         'placeholder':'Password',
    #         'required':'true'
    #     }))
    # password2 = forms.CharField(label="비밀번호 확인",
    #     widget=forms.PasswordInput(attrs={
    #         'placeholder':'Password Confirmation',
    #         'required': 'true',
    #     }),
    #     help_text="Enter the same password as above, for verification"
    #     )
    # business_number = forms.IntegerField(required=True, 
    #     widget=forms.NumberInput(attrs={
    #         'required': 'true',
    #         'placeholder':'사업자등록번호.'}))
        

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'bizNumber',)
    
    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.address = self.cleaned_data['address']
        user.bizNumber = self.cleaned_data['bizNumber']
        if commit:
            user.save()
        return user


# class CustomUserChangeForm(UserChangeForm):
#     email = forms.EmailField(required=True)
#     address = forms.CharField(required=True)
    
#     class Meta:
#         model = get_user_model()
#         fields = ('username', 'email', 'address',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('username', 'email', )

class ProfileForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False)
    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ('nickname', 'profile_photo', 'address', 'bizNumber', )
