from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.models import User
# from django.contrib.auth.views import LoginView as auth_login
# from allauth.socialaccount.models import SocialApp
# from allauth.socialaccount.templatetags.socialaccount import get_providers
from food.models import Food
from django.views import View
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Profile

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': '이미 사용중인 아이디입니다.'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                nickname = request.POST['nickname']
                address = request.POST['address']
                bizNumber = request.POST['bizNumber']
                # photo = photo받아오는거 추가해야함
                profile = Profile(user=user, nickname=nickname, address=address, bizNumber=bizNumber)
                profile.save()
                auth.login(request, user)
                return redirect('food:home')
    return render(request, 'signup.html')

def user_delete(request):
    try:
        deleted_user = User.objects.all().filter(username=request.user)
        deleted_user.delete()
        return redirect('home')

    except Exception:
        return render(request, 'profile.html', {'error':'탈퇴실패'})
    return render(request, 'home.html')

def profilepage(request):
    return render(request, 'profile.html')

# 내 글 조회 및 관리
def mypost(request):
    # food_detail = get_object_or_404(Profile, pk=user_id)
    mypost = Food.objects
    mypost_list = Food.objects.all().filter(author=request.user)
    print(type(mypost_list))
    return render(request, 'myposts.html', {'mypost_list':mypost_list})

def user_profile(request):
    user = User.objects.all().filter(username=request.user)
    profile = Profile.objects.all().filter(user=request.user)
    return render(request, 'profile_detail.html', {'profile':profile})

# def update(request):
#     user = User.objects.all().filter(username=request.user)
#     profile = Profile.objects.all().filter(user=request.user)
#     if request.method == 'POST':
# #  profile.html에 password확인해서 사용자 맞으면 profile_update.html에 들어갈 수 있게 하기 
#             first_name = request.POST['first_name']
#             last_name = request.POST['last_name']
#             nickname = request.POST['nickname']
#             address = request.POST['address']
#             user = User(first_name=first_name, last_name=last_name)
#             user.save()
#             profile = Profile(nickname=nickname, address=address)
#             profile.save()
#             return redirect('profile')
#     return render(request, 'profile_update.html', {'profile':profile, 'user':user})
            
        
        # if form.is_valid():
        #     new_profile = form.save(commit=False)
        #     new_profile.save()
        #     return redirect('profile', profile_id=profile_id)
        # else :
        #     form = ProfileForm(instance=user_profile)
        # return render(request, 'profile_update.html', {'form':form})

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

# 회원가입과 동시에 로그인 구현 참고: https://github.com/YeongBaeeee/practice/wiki/26-OAuth-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85%EA%B3%BC-%EB%8F%99%EC%8B%9C%EC%97%90-%EB%A1%9C%EA%B7%B8%EC%9D%B8
# def kakaoLogin(request):
#     providers = []
#     for provider in get_providers():
#         try:
#             provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
#         except SocialApp.DoesNotExist:
#             provider.social_app - None
#             providers.append(provider)
#             return auth_login(request, authentication_form=Profile, template_name='login.html', extra_context={'providers':providers})
            

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return render(request, 'login.html')

def socialLogin(request):
   login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'
   client_id = 'a1b93304238ae08e26b2f453e90b8481'
   redirect_uri = 'http://localhost:8000/accounts/oauth'
   login_request_uri += 'client_id=' + client_id
   login_request_uri += '&redirect_uri=' + redirect_uri
   login_request_uri += '&response_type=code'
   request.session['client_id'] = client_id
   request.session['redirect_uri'] = redirect_uri
   return redirect(login_request_uri)

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