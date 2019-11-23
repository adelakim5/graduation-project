from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User, Group
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.views import LoginView as auth_login
# from allauth.socialaccount.models import SocialApp
# from allauth.socialaccount.templatetags.socialaccount import get_providers
from food.models import Food
from django.views import View
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Profile
# from django import template

# register = template.Library()
# @register.filter(name='has_group')
# def has_group(user, group_name):
#     return user.groups.filter(name=profile_user).exists()

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                the_user = User.objects.get(username=request.POST['username'])
                user = Profile.objects.get(user=the_user)
                return render(request, 'signup.html', {'error': '이미 사용중인 아이디입니다.'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                user.has_perm('profile_status')
                nickname = request.POST['nickname']
                address = request.POST['address']
                bizNumber = request.POST['bizNumber']
                profile = Profile(user=user, nickname=nickname, address=address, bizNumber=bizNumber)
                profile.save()
                auth.login(request, user)
                messages.success(request, '가입되었습니다.')
                return redirect('home')
    return render(request, 'signup.html')

def user_delete(request):
    try:
        deleted_user = User.objects.all().filter(username=request.user)
        deleted_user.delete()
        return redirect('home')
    except Exception:
        return render(request, 'profile.html', {'error':'탈퇴실패'})
    return render(request, 'home.html')

def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        profile.nickname = request.POST['nickname']
        profile.address = request.POST['address']
        profile.bizNumber = request.POST['bizNumber']
        profile.save()
        return redirect('profile_detail')
    else:
        return render(request, 'profile_update.html')

def profilepage(request):
    return render(request, 'profile.html')

def user_profile(request):
    user = User.objects.all().filter(username=request.user)
    profile = Profile.objects.all().filter(user=request.user)
    return render(request, 'profile_detail.html', {'profile':profile})

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

   
# def friends(request):
#     if request.method == 'POST':
#         Authorization = 'KakaoAK ' + '1003f4e4429fec7aca912b2c74e0f659'
#         push_url = 'https://kapi.kakao.com/v1/push/register'
#         push_url += "Authorization: "+Authorization
#         push_url += "uuid=" + str(User.objects.get(username=request.user).pk)
#         push_url += "&device_id=" + "0f365b39-c33d-39be-bdfc-74aaf553447"
#         push_url += "&push_type=" + "gcm"
#         push_url += "push_token=" + "BLTwLkIR7wbADh0ef0Geri794RrmaPGGQQe7VLXLXIJYeo_0zieE6qx264UIX9WfwPriQnbUBbeOpcpquny-tHM"
        
#         print(push_url)
#         return redirect(push_url)
    
    # return render(request, 'hello.html')
    
    