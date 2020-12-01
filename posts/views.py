from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone 
from django.template import RequestContext
from django.db.models.functions import Replace
from django.db.models import Value
# models
from .models import *
from carts.models import *
from accounts.models import *
# message
from .forms import *
from decimal import Decimal
from allauth.socialaccount.models import SocialAccount, SocialToken
import requests, json
# coolsms
import sys
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
# stream
from django.http import HttpResponse
from myurl import Url

isLocal = Url(False).getUrl()

def stream(request):
    profile = Profile.objects.get(user=request.user)
    cart2 = Cart2.objects.all().filter(receiver=profile).filter(status="1")

    if cart2:
        return HttpResponse(
            "data: hi\n\n",
            content_type='text/event-stream'
        )

# 매장이 보는 게시글관리 
def viewMyPostList(request):
    the_author = Profile.objects.get(user=request.user)
    post_list = Food.objects.all().filter(author=the_author)
    return render(request, 'myPostList.html', {'post_list':post_list})

# 더보기 
def detail(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    print(request.user)
    if request.user.is_authenticated:
        pastCart = ('true' if Cart2.objects.all().filter(sender=request.user) else 'false')
        return render(request, 'detail.html', {'food':food_detail,'past_cart':pastCart})
    return render(request, 'detail.html', {'food':food_detail })

# 후기
def addComments(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = food_detail
            comment.save()
            return redirect('detail', food_id=food_id)
    else:
        form = CommentForm()
    return render(request, 'comment.html', {'form':form})

# 매장 글 등록
def writeNewPost(request):
    if request.method == 'POST':
        form = FoodPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            the_author = Profile.objects.get(user=request.user)
            post.author = the_author
            post.pub_date=timezone.now()
            post.save()
            return redirect('viewMyPostList')
    else:
        form = FoodPost()
    return render(request,'writeNewPost.html', {'form':form})

#  매장 글 수정
def edit(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    if request.method == 'POST':
        form = FoodPost(request.POST, request.FILES, instance=food_detail)
        if form.is_valid():
            post = form.save(commit=False)
            the_author = Profile.objects.get(user=request.user)
            post.author = the_author
            post.pub_date=timezone.now()
            post.save()
            return redirect('detail', food_id=food_id)
            # 게시글 관리에서 수정할 수 있게 옮기자(게시글 관리 페이지 만들면)
    else:
        form = FoodPost(instance=food_detail)
    return render(request, 'edit.html', {'form':form})     

# 매장이 자기 글 삭제 
def delete(request, food_id):
    deleted_food = get_object_or_404(Food, pk=food_id)
    if request.method == 'POST':
        deleted_food.delete()
        return redirect('viewMyPostList')

