from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.urls import reverse_lazy
from .forms import SignupForm, UserForm, ProfileForm
# from .forms import SignupForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.

class ProfileUpdateView(View):
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        user_form = UserForm(initial={
            'username': user.username,
            'email': user.email,
        })

        if hasattr(user, 'profile'):
            profile = user.profile
            profile_form = ProfileForm(initial={
                'nickname':profile.nickname,
                'profile_photo': profile.profile_photo,
                'address':profile.address,
                'bizNumber':profile.bizNumber,
            })
        else:
            profile_form = ProfileForm()

        return render(request, 'profile_update.html', {'user_form':user_form, 'profile_form':profile_form})

# 수정(저장)버튼 눌렀을 때 넘겨받은 데이터를 저장하는 post메소드
    def post(self, request):
        u = User.objects.get(id=request.user.pk) #로그인 중인 사용자 객체 받아옴
        user_form = UserForm(request.POST, instance=u) # 기존의 것의 업데이트하는 것 이므로 기존의 인스턴스를 넘겨줘야한다. 기존의 것을 가져와 수정하는 것

        #User form
        if user_form.is_valid():
            user_form.save()

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile) # 기존의 것 가져와 수정
        
        else:
            profile_form = ProfileForm(request.POST, request.FILES) #새로 만드는 것

        #profile form
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = u
            profile.save()

        return redirect('profile', pk=request.user.pk) #수정된 화면 보여주기


class CreateUserView(CreateView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('signup_done')

class RegisteredView(TemplateView):
    template_name = 'signup_done.html'


# def login(request):
#     if request.method == 'POST':
#         login_form = AuthenticationForm(request, request.POST)
#         if login_form.is_valid():
#             auth_login(request, login_form.get_user())
#         return redirect('home')
#     else:
#         login_form = AuthenticationForm()
#     return render(request, 'login.html', {'login_form':login_form})


class ProfileView(DetailView):
    context_object_name = 'profile_user'
    model = User
    template_name = 'profile.html'

# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             try:
#                 user = User.objects.get(username=request.POST['username'])
#                 return render(request, 'signup.html', {'error' : '이미 사용중인 아이디 입니다.'})
#             except User.DoesNotExist:
#                 user = User.objects.create_user(
#                     request.POST['username'], 
#                     password=request.POST['password1'])
#                 auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#                 return redirect('home')
#         else:
#             return render(request, 'signup.html', {'error': '비밀번호가 다릅니다.'})
#     else:
#         return render(request, 'signup.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error' : '아이디 또는 비밀번호가 다릅니다.'})
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'login.html')

#def socialLogin(request):
   # login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'
   # client_id = 'a1b93304238ae08e26b2f453e90b8481'
   # redirect_uri = 'http://127.0.0.1:8000/accounts/oauth'
   # login_request_uri += 'client_id=' + client_id
   # login_request_uri += '&redirect_uri=' + redirect_uri
   # login_request_uri += '&response_type=code'
   # request.session['client_id'] = client_id
   # request.session['redirect_uri'] = redirect_uri
   # return redirect(login_request_uri)

def oauth(request):           
    code = request.GET['code']
    print('code = '+ str(code))
    
    client_id = request.session.get('client_id')
    redirect_uri = request.session.get('redirect_uri')

    access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
 
    access_token_request_uri += "client_id=" + client_id
    access_token_request_uri += "&redirect_uri=" + redirect_uri
    access_token_request_uri += "&code=" + code
 
    print(access_token_request_uri)
    
    return redirect('home')