from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import *
from accounts.models import *
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.utils import timezone 
import requests, json, sys


# Create your views here.
# 고객의 장바구니
def customersPresentCarts(request):
    request_list = Cart.objects.all().filter(sender=request.user)
    return render(request, 'customers/myCart.html', {'request_list':request_list})

# 매장이 보는 나의 요청온내역 
def restaurantReceiveCarts(request):
    the_receiver = Profile.objects.get(user=request.user)
    requested_list = Cart2.objects.all().filter(receiver=the_receiver)
    customer_list = []
    for customer in requested_list:
        customer_list.append(Customer.objects.get(customer=User.objects.get(username=customer.sender)))
    
    return render(request, 'restaurants/receiveCarts.html', {'request_list':requested_list,'customer_list':customer_list})

# 매장이 보는 지난 요청 내역
def restaurantPastReceivedCarts(request):
    me = Profile.objects.get(user=request.user)
    past = Cart3.objects.all().filter(receiver=me)
    past = past.order_by('-date')
    cus = Customer.objects.all().filter(whose=me)
    form = CustomerForm(request.POST)
    # 고객등록을 누르면 Customer로 저장 
    if request.method == 'POST':
        sender = User.objects.get(username=request.POST['sender'])
        receiver = Profile.objects.get(user=request.user)
        if cus.filter(customer=sender):
            messages.add_message(request, messages.ERROR, '이미 등록된 고객입니다.')
            return redirect('past')
        else:
            if form.is_valid():
                customer = form.save(commit=False)
                customer.customer = sender
                customer.whose = receiver
                customer.reason = request.POST['reason']
                customer.others = request.POST['others']
                customer.save()
                return redirect('restaurantCustomerlist')
    return render(request, 'restaurants/myPastReceivedCartsList.html', {'past':past, 'form':form})

# 고객 수정, 관리
def restaurantManageCustomers(request, customer_id):
    customer_detail = get_object_or_404(Customer, pk=customer_id)
    # 등록을 누르면 
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer_detail)
        if form.is_valid():
            custom = form.save(commit=False)
            custom.whose = Profile.objects.get(user=request.user)
            custom.reason = request.POST['reason']
            custom.others = request.POST['others']
            custom.customer = User.objects.get(username=customer_detail.customer)
            custom.save()
            return redirect('restaurantCustomerlist')
    else:
        form = CustomerForm(instance=customer_detail)
        return render(request, 'restaurants/manageCustomers.html', {'form':form, 'customer':customer_detail})

# 고객 조회
def restaurantCustomerlist(request):
    me = Profile.objects.get(user=request.user)
    mycustomers = Customer.objects.all().filter(whose=me)
    return render(request, 'restaurants/myCustomerList.html', {'mycustomers':mycustomers})
    
    # how_many는 Cart3의 receiver=me, sender가 customer의 customer의 개수 

# 요청: 장바구니에 담는 과정 
def customerAddCart(request, food_id):
    food_detail = get_object_or_404(Food, pk=food_id)
    if request.method == 'POST':
        if Cart.objects.all().filter(sender=request.user).count() != 0:
            # print(True)
            cartlist = Cart.objects.all().filter(sender=request.user)
            # print(cartlist)
            cartlist.delete()
            people = request.POST['people']
            total_price = request.POST['total_price']
            sender = request.user
            receiver = food_detail.author
            the_title = Food.objects.get(title=food_detail.title)
            phone = request.POST['phoneNum']
            cart = Cart(sender=request.user, people=people, total_price=total_price, receiver=receiver, title=the_title,phone=phone)
            cart.save()
            return redirect('customersPresentCarts')
        else: 
            print(False)
            people = request.POST['people']
            total_price = request.POST['total_price']
            sender = request.user
            receiver = food_detail.author
            the_title = Food.objects.get(title=food_detail.title)
            phone = request.POST['phoneNum']
            cart = Cart(sender=request.user, people=people, total_price=total_price, receiver=receiver, title=the_title,phone=phone)
            cart.save()
            return redirect('customersPresentCarts')
    return render(request, '../posts/detail.html', {'error':'요청실패', 'food':food_detail})

def requestFail(request):
    return render(request, 'customer/requestFail.html')

# 결제준비를 마친 고객이 결제 완료되었다는 문구를 보는 페이지 
def requestSuccess(request):
    access_token = SocialToken.objects.get(account__user=request.user, account__provider="kakao").token
    pg_token = request.GET['pg_token']
    cart2 = Cart2.objects.get(sender=request.user)
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        'Authorization': 'Bearer ' + str(access_token),
        'Content-Type':'application/x-www-form-urlencoded;charset=utf-8'
    }
    data = {
        "cid": "TC0ONETIME",
        "partner_order_id": cart2.order_id,
        "partner_user_id": cart2.receiver,
        "pg_token": pg_token,
        "tid": cart2.tid
    }
    res = requests.post(URL,headers=headers,data=data)
    
    if res.status_code == 200:
        cart2 = Cart2.objects.get(sender=request.user)
        cart2.status = "1"
        cart2.save()
        return render(request, 'check_success.html')
    else:
        cart2 = Cart2.objects.get(sender=request.user)
        cart2.status = "-1"
        cart2.save()
        return redirect('requestFail')

# 고객의 장바구니 --> 고객이 취소하고 돌아가기 누를 때  
def customerCancelCart(request, cart_id):
    cancel_cart = get_object_or_404(Cart, pk=cart_id)
    if request.method == 'POST':
        cancel_cart.delete()
        return redirect('home')

def customerSendCartToRestaurant(request):
    access_token = SocialToken.objects.get(account__user=request.user, account__provider="kakao").token
    # print(access_token)
    partner_user_id = Profile.objects.get(nickname=request.POST['receiver'])
    # print(partner_user_id)
    quantity = request.POST['people']
    # print(quantity)
    total_amount = request.POST['total_price']
    # print(total_amount)
    item_name = Food.objects.get(title=request.POST['title'])
    # print(item_name)
    partner_order_id = Cart.objects.get(id=request.POST['cart_id']).id
    # print(partner_order_id)
    phone_number = request.POST['phoneNumber']
    # print(phone_number)
    data = {
        "cid": "TC0ONETIME",
        "partner_order_id": partner_order_id,
        "partner_user_id": partner_user_id,
        "item_name": item_name,
        "quantity": quantity,
        "total_amount": total_amount,
        "vat_amount": 0,
        "tax_free_amount": 0,
        "approval_url": "%s/success/" % isLocal,
        "fail_url": "%s/fail" % isLocal,
        "cancel_url": "%s/fail" % isLocal   
    }
    URL = 'https://kapi.kakao.com/v1/payment/ready'
    ## http header를 보내는데, 여기에 Content-Type이나 권한인증을 위한 Token
    headers = {
        'Authorization': 'Bearer ' + str(access_token),
        'Content-Type':'application/x-www-form-urlencoded;charset=utf-8'
    }
    res = requests.post(URL,headers=headers,data=data)
    # print(res.status_code)
    # 받아온 데이터를 Json => Dict으로 바꿈.(파이썬에서 사용 가능하게)
    if res.status_code == 200:
        resp = json.loads(res.text)
        cart2 = Cart2(
            tid=resp['tid'],order_id=partner_order_id,
            sender=request.user, receiver=partner_user_id, people=quantity, 
            total_price=total_amount, request_date=timezone.now(), title=item_name,status="0",phone=phone_number)
        cart2.save()
        cart = Cart.objects.all().filter(sender=request.user).filter(receiver=partner_user_id)
        cart.delete()
        # print("@@@@@@@@@@@ order id = {} , tid = {}".format(partner_order_id , resp['tid']))
        return redirect(resp['next_redirect_pc_url'])
    else:
        return redirect('requestFail')

    # 매장이 거절    
def restaurantCancelCart(request, cart2_id):
    cart2 = get_object_or_404(Cart2, order_id=cart2_id)
    access_token = SocialToken.objects.get(account__user=cart2.sender, account__provider="kakao").token
    if request.method == 'POST':
        # 거절을 누른 경우
        cart2.status == "-1"
        headers = {
                    'Authorization': 'Bearer ' + str(access_token),
                    'Content-Type':'application/x-www-form-urlencoded;charset=utf-8'
                }
        data = {
                    "cid": "TC0ONETIME",
                    "partner_order_id": cart2.order_id,
                    "cancel_amount": cart2.total_price,
                    "cancel_vat_amount": 0,
                    "cancel_tax_free_amount": 0,
                    "tid": cart2.tid
                }
        URL = 'https://kapi.kakao.com/v1/payment/cancel'
        res = requests.post(URL,headers=headers,data=data)
            
        sender = cart2.sender
        receiver = cart2.receiver
        order_id = cart2.order_id
        people = cart2.people
        total_price = cart2.total_price
        date = timezone.now()
        title = cart2.title
        status = '-1'
        cart3 = Cart3(sender=sender, receiver=receiver, order_id=order_id, people=people, total_price=total_price, date=date, title=title, status=status)
        cart3.save()
        cart_of_sender = Cart.objects.all().filter(id=cart2_id)
        cart_of_sender.delete()
        cart2.delete()
        return redirect('restaurantReceiveCarts')

# 매장이 승인
def restaurantAcceptCart(request, cart2_id):
    cart2_detail = get_object_or_404(Cart2, order_id=cart2_id)
    if request.method == 'POST':
        api_key = "NCSMT6MABSKAUNEP"
        api_secret = "KRXVXII9XJ7NNQ2APASDXT9MEZNGYX1K"
    
        minute = request.POST['minute']
        
        params = dict()
        params['type'] = 'sms'
        params['to'] = cart2_detail.phone
        params['from'] = '010-3594-0227'
        params['text'] = '[궁동예약]요청이 승인되었습니다. 예상대기시간:' + minute + '분'
        
        cool = Message(api_key, api_secret)
        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)

    
        sender = cart2_detail.sender
        receiver = cart2_detail.receiver
        order_id = cart2_detail.order_id
        people = cart2_detail.people
        total_price = cart2_detail.total_price
        date = timezone.now()
        title = cart2_detail.title
        status = '1'
        cart3 = Cart3(sender=sender, receiver=receiver, order_id=order_id, people=people, total_price=total_price, date=date, title=title, status=status)
        cart3.save()
        cart_of_sender = cart2_detail
        cart_of_sender.delete()
        return redirect('restaurantReceiveCarts')
    
        sys.exit()


