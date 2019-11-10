from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator
from django.utils import timezone 
from .forms import *
from decimal import Decimal
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from accounts.models import *
from allauth.socialaccount.models import SocialAccount, SocialToken
import requests, json
# Create your views here.


def home(request):
    foods = Food.objects
    food_list = Food.objects.all()
    print(type(food_list))
    paginator = Paginator(food_list,4)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'foods':foods, 'posts':posts})

def myCart(request):
    requests = Cart.objects
    request_list = Cart.objects.all().filter(sender=request.user)
    # print(type(request_list))
    return render(request, 'myCart.html', {'request_list':request_list})

# def myCart_for_owner(request):
#   notification = Cart.objects
#   notifications = Cart.objects.all().filter(reciever=request.user)
#   return render(request, 'myCart.html, {'notifications':notifications})
#   페이지를 따로 만들어야 하는지, 아님 같은 페이지안에 if문 줘서 local 회원이랑 social회원이랑 구분해서 안보이게 할 수 있는지 알아보기

def detail(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    return render(request, 'detail.html', {'food':food_detail})

@login_required
def add_comment_to_food(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=food_detail)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = User.objects.get(username=request.user)
            # 대체 왜... Comment 모델의 author는 Profile로 명시하지 않은 앤데.. 왜 Profile instance만 가능할까...
            comment.post = food_detail
            comment.save()
            return redirect('detail', food_id=food_id)
        else:
            form = CommentForm(instance=food_detail)
        return render(request, 'comment.html', {'form':form})

@login_required
def cart(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    # 현재 페이지의 author를 어떻게 가져오지?
    if request.method == 'POST':
        people = request.POST['people']
        total_price = request.POST['total_price']
        sender = request.user
        receiver = food_detail.author
        the_title = Food.objects.get(title=food_detail.title)
        # request_date = timezone.now()
        cart = Cart(sender=request.user, people=people, total_price=total_price, receiver=receiver, title=the_title)
        cart.save()
        return redirect('myCart')
        # my내역에서 확인할 수 있도록 페이지 만들고 바꾸기
    return render(request, 'detail.html', {'error':'요청실패', 'food':food_detail})

def foodpost(request):
    if request.method == 'POST':
        form = FoodPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            # post.image = request.FILES['image']
            the_author = Profile.objects.get(user=request.user)
            post.author = the_author
            # post.author = request.user
            post.pub_date=timezone.now()
            post.save()
            return redirect('home')
    else:
        form = FoodPost()
    return render(request,'new.html', {'form':form})

def edit(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    if request.method == 'POST':
        form = FoodPost(request.POST, request.FILES, instance=food_detail)
        if form.is_valid():
            post = form.save(commit=False)
            # post.image = request.FILES['image']
            the_author = Profile.objects.get(user=request.user)
            post.author = the_author
            post.pub_date=timezone.now()
            post.save()
            return redirect('detail', food_id=food_id)
            # 게시글 관리에서 수정할 수 있게 옮기자(게시글 관리 페이지 만들면)
    else:
        form = FoodPost(instance=food_detail)
    return render(request, 'edit.html', {'form':form})        

            
def search(request):
    search = request.GET['searchkeyword']
    posts = Food.objects.filter(title__icontains=search) | Food.objects.filter(category__icontains=search) | Food.objects.filter(category2__icontains=search) 
    return render(request,'search.html',{'posts':posts})

def delete(request, food_id):
    deleted_food = get_object_or_404(Food, pk=food_id)
    deleted_food.delete()
    return redirect('home')
    # 게시글 관리에서 삭제할 수 있게 옮기기

@login_required
def checkplz(request):
    access_token = SocialToken.objects.get(account__user=request.user, account__provider="kakao").token
    partner_user_id = Profile.objects.get(nickname=request.POST['receiver'])
    quantity = request.POST['people']
    total_amount = request.POST['total_price']
    item_name = request.POST['title']
    partner_order_id = request.POST['cart_id']
    data = {
        "cid": "TC0ONETIME",
        "partner_order_id": partner_order_id,
        "partner_user_id": partner_user_id,
        "item_name": item_name,
        "quantity": quantity,
        "total_amount": total_amount,
        "vat_amount": 0,
        "tax_free_amount": 0,
        "approval_url": "http://localhost:8000/success/",
        "fail_url": "http://localhost:8000/fail",
        "cancel_url": "http://localhost:8000/fail"   
    }
    URL = 'https://kapi.kakao.com/v1/payment/ready'
    ## http header를 보내는데, 여기에 Content-Type이나 권한인증을 위한 Token
    headers = {
        'Authorization': 'Bearer ' + str(access_token),
        'Content-Type':'application/x-www-form-urlencoded;charset=utf-8'
    }
    res = requests.post(URL,headers=headers,data=data)
    ## 받아온 데이터를 Json => Dict으로 바꿈.(파이썬에서 사용 가능하게)
    print(res.text)
    resp = json.loads(res.text)
    return redirect(resp['next_redirect_pc_url'])
    

# def success(request):
#     return render(request, 'check_success.html')

def fail(request):
    return render(request, 'check_fail.html')

def successCart(request):
    request_list = Cart.objects.get(sender=request.user)
    if request.method == 'POST':
        sender = User.objects.get(username=request.POST['sender'])
        receiver = Profile.objects.get(nickname=request.POST['receiver'])
        the_title = Food.objects.get(title=request.POST['title'])
        people = request.POST['people']
        total_price = request.POST['total_price']
        # request_date = request.timezone.now()
        successCart = SuccessCart(sender=sender, people=people, total_price=total_price, receiver=receiver, title=the_title)
        successCart.save()
        return redirect('home')
    else:
        return render(request, 'check_success.html', {'error':'매장에 요청 들어가기 실패', 'requests':request_list})

        
